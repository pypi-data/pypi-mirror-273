import json
import os
import uuid
from datetime import datetime

from carbon_registry_indexer.models import enums, target
from . import utils, constants

import pandas as pd

def gs_projects_upsert(df, data_dir, table_name, co_benefits_file_name, estimations_file_name):
    """
    Process Gold Standard projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    co_benefits_csv_path = os.path.join(data_dir, co_benefits_file_name + ".csv")
    estimations_csv_path = os.path.join(data_dir, estimations_file_name + ".csv")

    # schema
    project_schema = target.Project.__table__.columns.keys()
    co_benefits_schema = target.CoBenefit.__table__.columns.keys()
    estimations_schema = target.Estimation.__table__.columns.keys()


    sdg_goals = df['Sustainable Development Goals']
    estimated_annual_credits = df['Estimated Annual Credits']
    existing_columns = [col for col in project_schema if col in df.columns]
    country = df['country']
    utils.map_enums(table_name, df)
    df = df[existing_columns]
    df['current_registry'] = enums.Registries.GoldStandard.name
    df['registry_of_origin'] = enums.Registries.GoldStandard.name
    df_cleaned = df.where(pd.notnull(df), None)

    if not df_cleaned.empty:
        try:
            df_cleaned['cmhq_project_id'] = ["GS-" + str(pid) for pid in df_cleaned['project_id']]
            cmhq_project_ids = df_cleaned['cmhq_project_id']
            df_cleaned['project_tags'] = {}

            co_benefits = []
            estimations = []

            for index, row in df_cleaned.iterrows():

                project_tags = {}
                for k, v in constants.gs_project_tags_cols.items():
                    if k in row and not pd.isna(row[k]):
                        project_tags.update({k: row[k]})
                df.loc[index, 'project_tags'] = json.dumps(project_tags)

                if sdg_goals[index]:
                    if isinstance(sdg_goals[index], int):
                        sdg_goal = [sdg_goals[index]]
                    elif isinstance(sdg_goals[index], str):
                        sdg_goal = sdg_goals[index].split(',')
                    else:
                        sdg_goal = []

                    for goal in sdg_goal:
                        cb = utils.co_benefit_number_reverse_mapping(int(goal))
                        if not cb:
                            continue
                        co_benefit = {
                            "cmhq_project_id": row['cmhq_project_id'],
                            "co_benefit": cb
                        }
                        co_benefits.append(co_benefit)
                if estimated_annual_credits[index]:
                    estimation = {
                        "cmhq_project_id": row['cmhq_project_id'],
                        "unit_count": estimated_annual_credits[index],
                    }
                    estimations.append(estimation)

        except Exception as e:
            print(f"Error processing projects: {e}")

    if co_benefits:
        co_benefits_df = pd.DataFrame(co_benefits)
        co_benefits_df['co_benefit_id'] = co_benefits_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'co_benefit']),
            axis=1
        )
        utils.update_csv(co_benefits_df, 
                         co_benefits_csv_path,
                         co_benefits_schema,
                         check_schema=True)
        print(f"Processed {len(co_benefits)} co-benefits. Data saved to {co_benefits_csv_path}.")

    if estimations:
        estimations_df = pd.DataFrame(estimations)
        estimations_df['estimation_id'] = estimations_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
            axis=1
        )
        utils.update_csv(estimations_df, 
                         estimations_csv_path,
                         estimations_schema,
                         check_schema=True)
        print(f"Processed {len(estimations)} estimations. Data saved to {estimations_csv_path}.")

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df_cleaned)} projects. Data saved to {target_csv_path}.")

    return country, cmhq_project_ids

def gs_project_locations_upsert(df, data_dir, table_name, countries, cmhq_project_ids):
    """
    Process Gold Standard project locations data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    schema = target.ProjectLocation.__table__.columns.keys()
    existing_columns = [col for col in schema if col in df.columns]
    df = df[existing_columns]

    df['cmhq_project_id'] = cmhq_project_ids
    df['country'] = countries

    utils.map_enums(table_name, df)
    df_cleaned = df.where(pd.notnull(df), None)
    df_cleaned['project_location_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
        axis=1
    )

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} project locations. Data saved to {target_csv_path}.")
    
def gs_issuance_upsert(df, data_dir, table_name, projects_file_name):
    """
    Process Gold Standard issuances data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    gs_project_ids = [i for i in df['project_id']]
    schema = target.Issuance.__table__.columns.keys()
    
    df_cleaned = df.where(pd.notnull(df), None)
    
    projects_sheet = pd.read_csv(projects_file_path)
    cmhq_project_ids = {projects_sheet['project_id'][i]: projects_sheet['cmhq_project_id'][i] for i in range(len(projects_sheet)) if projects_sheet['project_id'][i] in gs_project_ids}
    
    df_cleaned = df_cleaned[df_cleaned['project_id'].apply(lambda x: x in cmhq_project_ids)]
    for index, row in df_cleaned.iterrows():
        df_cleaned.at[index, 'cmhq_project_id'] = cmhq_project_ids.get(row['project_id'])

    existing_columns = [col for col in schema if col in df_cleaned.columns]
    df_cleaned = df_cleaned[existing_columns]
    df_cleaned['issuance_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'issuance_start_date', 'issuance_end_date', 'vintage_year']),
        axis=1
    )
    df_cleaned = df_cleaned.drop_duplicates(subset=['issuance_id'])

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} issuances. Data saved to {target_csv_path}.")


def gs_units_upsert(df, unit_cols, data_dir, table_name, projects_file_name, issuance_file_name, labels_file_name):
    """
    Process Gold Standard units data and save to csv.
    """
    gs_project_ids = [i for i in df['project_id']]
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    issuance_file_path = os.path.join(data_dir, issuance_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")

    # schema
    units_schema = target.Unit.__table__.columns.keys()
    labels_schema = target.Label.__table__.columns.keys()

    utils.map_enums(table_name, df)

    project_id_mapping = {}
    projects_sheet = pd.read_csv(projects_file_path)
    for _, row in projects_sheet.iterrows():
        project_id_mapping[row['project_id']] = row['cmhq_project_id']

    issuance_id_mapping = {}

    df['unit_block_start'] = None
    df['unit_block_end'] = None
    issuances_sheet = pd.read_csv(issuance_file_path)
    cmhq_project_ids = list(project_id_mapping.values())
    for _, row in issuances_sheet.iterrows():
        if row['cmhq_project_id'] in cmhq_project_ids:
            issuance_id_mapping[row['cmhq_project_id']] = row['issuance_id']
    label_records = []
    records = []
    for index, row in df.iterrows():
        row['unit_block_start'] = row['Serial Number']
        row['unit_block_end'] = row['Serial Number']
        row_dict = {col: (None if pd.isna(value) else value) for col, value in row.items()}
        gs_project_id = gs_project_ids[index]
        cmhq_project_id = project_id_mapping.get(gs_project_id)
        if cmhq_project_id is None:
                print(f"Project related to {gs_project_id} not found in the database. Skipping this row.")
                continue
            
        cmhq_issuance_id = issuance_id_mapping.get(cmhq_project_id)
        if cmhq_issuance_id is None:
            print(f"Issuance related to {cmhq_project_id} not found in the database. Skipping this row.")
            continue

        if row['Eligible for CORSIA?'] == 'Yes':
            label_records.append({
                'label_id': uuid.uuid4(),
                "label_type": enums.LabelType.Certification.name,
                'label': 'CORSIA',
                'cmhq_project_id': cmhq_project_id,
            })

        row_dict['issuance_id'] = cmhq_issuance_id
        row_dict['unit_tags'] = {}

        for sheet_col, db_col in unit_cols.items():
            if db_col != "unit_tags":
                row_dict[db_col] = row_dict.pop(sheet_col)
            else:
                if isinstance(row_dict[sheet_col], datetime):
                    row_dict[sheet_col] = row_dict[sheet_col].strftime("%Y-%m-%d")
    
                row_dict[db_col].update({sheet_col: row_dict.pop(sheet_col)})
        row_dict['unit_tags'] = json.dumps(row_dict['unit_tags'])
        records.append(row_dict)

    if label_records:
        utils.update_csv(label_records, 
                         labels_file_path, 
                         labels_schema, 
                         check_schema=True)
        print(f"Processed {len(label_records)} labels. Data saved to {labels_file_path}.")

    if records:
        df_cleaned = pd.DataFrame(records)
        df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
            lambda row: utils.generate_uuid_from_row(row, ['Serial Number', 'project_id', 'issuance_id', 'unit_status', 'issuance_date']),
            axis=1
        )
        # drop duplicates baaed on cmhq_unit_id
        df_cleaned = df_cleaned.drop_duplicates(subset=['cmhq_unit_id'])
        existing_columns = [col for col in units_schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        target_csv_path = os.path.join(data_dir, table_name + ".csv")
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {target_csv_path}.")
