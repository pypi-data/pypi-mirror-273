import json
import os
import uuid

from carbon_registry_indexer.models import enums, target
from . import utils, constants

import pandas as pd

def car_projects_upsert(df, data_dir, table_name, project_locations_file_name, labels_file_name, co_benefits_file_name, estimations_file_name):
    """
    Process CAR projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    project_locations_file_path = os.path.join(data_dir, project_locations_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")
    co_benefits_file_path = os.path.join(data_dir, co_benefits_file_name + ".csv")
    estimations_file_path = os.path.join(data_dir, estimations_file_name + ".csv")

    # schemas
    project_schema = target.Project.__table__.columns.keys()
    project_location_schema = target.ProjectLocation.__table__.columns.keys()
    label_schema = target.Label.__table__.columns.keys()
    co_benefit_schema = target.CoBenefit.__table__.columns.keys()
    estimation_schema = target.Estimation.__table__.columns.keys()
    
    df['project_status_date'] = None
    total_number_of_credits_registered = df['Total Number of Offset Credits Registered ']

    for index, row in df.iterrows():
        if row['project_status'] == "Listed":
            df.at[index, 'project_status_date'] = row['Project Listed Date']
        elif row['project_status'] == "Registered":
            df.at[index, 'project_status_date'] = row['Project Registered Date']
        

    utils.map_enums(table_name, df)
    country = df['country']
    country = utils.map_countries_to_enums(country)
    in_country_region = df['in_country_region']
    arb_ids = df['compliance_program_id']
    df_cleaned = df.where(pd.notnull(df), None)
    df_cleaned['cmhq_project_id'] = [pid for pid in df_cleaned['project_id']]
    df_cleaned['current_registry'] = enums.Registries.ClimateActionReserveCAR.name
    df_cleaned['registry_of_origin'] = enums.Registries.ClimateActionReserveCAR.name
    df_cleaned['validation_body'] = df_cleaned['validation_body'].apply(lambda x: x if x is not None else enums.ValidationBody.Other.name)
    df_cleaned['project_tags'] = None
    project_locations_list = []
    labels_list = []
    estimations_list = []
    co_benefits_list = []
    for index, row in df_cleaned.iterrows():
        if row['SDG Impact']:
            list_of_all_sdgs = row['SDG Impact'].split(";")
            for sdg in list_of_all_sdgs:
                sdg = sdg.split(".")[-1].strip()
                co_benefit = {
                    "cmhq_project_id": row['cmhq_project_id'],
                    "co_benefit": utils.co_benefit_reverse_mapping(sdg)
                }
                co_benefits_list.append(co_benefit)
        unit_count = total_number_of_credits_registered[index]
        if pd.isna(unit_count):
            unit_count = None
        estimation = {
            "cmhq_project_id": row['cmhq_project_id'],
            "unit_count": unit_count
        }
        estimations_list.append(estimation)
        project_tags = {}
        for k, v in constants.car_project_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                project_tags.update({k: row[k]})
        if project_tags:
            df_cleaned.at[index, 'project_tags'] = json.dumps(project_tags)
        if arb_ids[index] != 'NA':
            label = {
                "label_type": enums.LabelType.Certification.name,
                "label": "ARB compliant",
                "cmhq_project_id": row['cmhq_project_id']
            }
        elif df_cleaned['CORSIA Eligible'] == 'Yes':
            label = {
                "label_type": enums.LabelType.Certification.name,
                "label": "CORSIA eligible",
                "cmhq_project_id": row['cmhq_project_id']
            }
        project_location = {
            "cmhq_project_id": row['cmhq_project_id'],
            "country": country[index],
            "in_country_region": in_country_region[index],
        }
        if label:
            labels_list.append(label)
        project_locations_list.append(project_location)
            
    if project_locations_list:
        project_locations_df = pd.DataFrame(project_locations_list)
        project_locations_df['project_location_id'] = project_locations_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
            axis=1
        )
        utils.update_csv(project_locations_df, 
                         project_locations_file_path, 
                         project_location_schema, 
                         check_schema=True)
        print(f"Processed {len(project_locations_list)} project locations. Data saved to {project_locations_file_path}.")

    if co_benefits_list:
        cobenefits_df = pd.DataFrame(co_benefits_list)
        cobenefits_df['co_benefit_id'] = cobenefits_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'co_benefit']),
            axis=1
        )
        utils.update_csv(cobenefits_df, 
                         co_benefits_file_path, 
                         co_benefit_schema,
                         check_schema=True)
        print(f"Processed {len(co_benefits_list)} co-benefits. Data saved to {co_benefits_file_path}.")

    if estimations_list:
        estimations_df = pd.DataFrame(estimations_list)
        estimations_df['estimation_id'] = estimations_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
            axis=1
        )
        utils.update_csv(estimations_df, 
                         estimations_file_path,
                         estimation_schema,
                         check_schema=True)
        print(f"Processed {len(estimations_list)} estimations. Data saved to {estimations_file_path}.")

    if labels_list:
        labels_df = pd.DataFrame(labels_list)
        labels_df['label_id'] = labels_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']), 
            axis=1
        )
        utils.update_csv(labels_df, 
                         labels_file_path,
                         label_schema,
                         check_schema=True)
        print(f"Processed {len(labels_list)} labels. Data saved to {labels_file_path}.")

    if not df_cleaned.empty:
        existing_columns = [col for col in project_schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        utils.update_csv(df_cleaned,
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} projects. Data saved to {target_csv_path}.")
    

def car_issuances_upsert(df, data_dir, table_name, projects_file_name):
    """
    Process CAR issuances data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")

    schema = target.Issuance.__table__.columns.keys()

    df_cleaned = df.where(pd.notnull(df), None)
    projects_sheet = pd.read_csv(projects_file_path)
    cmhq_project_ids = {projects_sheet['project_id'][i]: projects_sheet['cmhq_project_id'][i] for i in range(len(projects_sheet))}
    df_cleaned['cmhq_project_id'] = [cmhq_project_ids[pid] for pid in df_cleaned['project_id']]
    df_cleaned['vintage_year'] = df_cleaned['vintage_year'].astype(int)

    existing_columns = [col for col in schema if col in df_cleaned.columns]
    df_cleaned = df_cleaned[existing_columns]
    df_cleaned['issuance_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'issuance_start_date', 'vintage_year']),
        axis=1
    )
    df_cleaned = df_cleaned.drop_duplicates(subset=['issuance_id'], keep='first')
    utils.update_csv(df_cleaned, 
                     target_csv_path, 
                     check_schema=False)
    print(f"Processed {len(df_cleaned)} issuances. Data saved to {target_csv_path}.")        


def car_units_issued_upsert(df, data_dir, table_name, projects_file_name, issuances_file_name, labels_file_name, status):
    """
    Process CAR units data and save to csv.
    """
    car_project_ids = [str(i) for i in df['project_id']]
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    issuance_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")
    schema = target.Unit.__table__.columns.keys()

    df['unit_status'] = [status for _ in range(len(df))]
    df['issuance_id'] = None
    df['unit_tags'] = None
    df['corresponding_adjustment_declaration'] = None
    df['corresponding_adjustment_status'] = None
    df['unit_block_start'] = None
    df['unit_block_end'] = None
    df['label_id'] = None
    projects_sheet = pd.read_csv(projects_file_path)
    if not os.path.exists(issuance_file_path):
        raise FileNotFoundError(f"Issuances file {issuance_file_path} not found.")
    issuance_sheet = pd.read_csv(issuance_file_path)
    projects = projects_sheet[projects_sheet['project_id'].isin(car_project_ids)]
    projects_mapping = {}
    for index, row in projects.iterrows():
        projects_mapping[row['project_id']] = row['cmhq_project_id']
    records = []
    for index, row in df.iterrows():
        if 'Offset Credit Serial Numbers' in row:
            if row['Offset Credit Serial Numbers']:
                df.loc[index, 'unit_block_start'] = row['Offset Credit Serial Numbers']
                df.loc[index, 'unit_block_end'] = row['Offset Credit Serial Numbers']
        try:
            if row['Corresponding Adjustment'] == 'Yes':
                df.loc[index, 'corresponding_adjustment_declaration'] = enums.CorrespondingAdjustmentDeclaration.Committed.name
                df.loc[index, 'corresponding_adjustment_status'] = enums.CorrespondingAdjustmentStatus.Completed.name
            elif row['Corresponding Adjustment'] == 'No':
                df.loc[index, 'corresponding_adjustment_declaration'] = enums.CorrespondingAdjustmentDeclaration.Unknown.name
                df.loc[index, 'corresponding_adjustment_status'] = enums.CorrespondingAdjustmentStatus.NotStarted.name
        except KeyError as e:
            print(f"Error updating corresponding_adjustment: {e}")
        
        try:
            cmhq_project_id = projects_mapping.get(row['project_id'])
            if not cmhq_project_id:
                raise Exception(f"No project found for project {row['project_id']}")
            
            issuance = issuance_sheet[
                (issuance_sheet['cmhq_project_id'] == cmhq_project_id) &
                (issuance_sheet['issuance_start_date'] == row['unit_status_date']) &
                (issuance_sheet['vintage_year'] == row['vintage_year'])    
            ]
            if issuance.empty:
                raise Exception(f"Issuance not found for project {cmhq_project_id}, {row['unit_status_date']} & {row['vintage_year']}")
            
            issuance_id = issuance['issuance_id'].values[0]
            print(f"Found issuance {issuance_id} for project {cmhq_project_id}")
            df.loc[index, 'issuance_id'] = issuance_id

        except Exception as e:
            print(f"Error fetching related issuance: {e}")
            continue

        try:
            if os.path.exists(labels_file_path):
                labels = pd.read_csv(labels_file_path)
                label = labels[labels['cmhq_project_id'] == cmhq_project_id]
                if not label.empty:
                    df.loc[index, 'label_id'] = label['label_id'].values[0]
        except Exception as e:
            print(f"Error fetching related Label: {e}")

        if "Protocol Version" in row:
            if row["Protocol Version"]:
                methodology = utils.car_map_methodology_enum(row["Protocol Version"])
                projects_sheet.loc[projects_sheet['cmhq_project_id'] == cmhq_project_id, "methodology"] = methodology
        
        unit_tags = {}

        for k, v in constants.car_unit_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                unit_tags.update({k: row[k]})
        
        df.loc[index, 'unit_tags'] = json.dumps(unit_tags)
        records.append(df.loc[index].to_dict())
    
    # update projects
    utils.direct_merge_and_update_csv(projects_sheet, projects_file_path)
    
    if records:
        df_cleaned = pd.DataFrame(records)
        df_cleaned = df_cleaned.where(pd.notnull(df_cleaned), None)
        df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
            lambda row: utils.generate_uuid_from_row(row, ['Offset Credit Serial Numbers', 'issuance_start_date', 'issuance_id', 'vintage_year', 'project_id', 'unit_status', 'unit_count']),
            axis=1
        )
        existing_columns = [col for col in schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        target_csv_path = os.path.join(data_dir, table_name + ".csv")
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {table_name}.csv.")

def car_units_retired_cancelled_upsert(df, data_dir, table_name, projects_file_name, issuances_file_name, labels_file_name, status):
    """
    Process CAR units data and save to csv.
    """
    car_project_ids = [str(i) for i in df['project_id']]
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    issuance_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")
    schema = target.Unit.__table__.columns.keys()

    df['unit_status'] = [status for _ in range(len(df))]
    df['issuance_id'] = None
    df['unit_tags'] = None
    df['corresponding_adjustment_declaration'] = None
    df['corresponding_adjustment_status'] = None
    df['unit_block_start'] = None
    df['unit_block_end'] = None
    df['label_id'] = None
    projects_sheet = pd.read_csv(projects_file_path)
    if not os.path.exists(issuance_file_path):
        raise FileNotFoundError(f"Issuances file {issuance_file_path} not found.")
    issuance_sheet = pd.read_csv(issuance_file_path)
    projects = projects_sheet[projects_sheet['project_id'].isin(car_project_ids)]
    projects_mapping = {}
    for index, row in projects.iterrows():
        projects_mapping[row['project_id']] = row['cmhq_project_id']
    records = []
    for index, row in df.iterrows():
        if 'Offset Credit Serial Numbers' in row:
            if row['Offset Credit Serial Numbers']:
                df.loc[index, 'unit_block_start'] = row['Offset Credit Serial Numbers']
                df.loc[index, 'unit_block_end'] = row['Offset Credit Serial Numbers']
        try:
            if row['Corresponding Adjustment'] == 'Yes':
                df.loc[index, 'corresponding_adjustment_declaration'] = enums.CorrespondingAdjustmentDeclaration.Committed.name
                df.loc[index, 'corresponding_adjustment_status'] = enums.CorrespondingAdjustmentStatus.Completed.name
            elif row['Corresponding Adjustment'] == 'No':
                df.loc[index, 'corresponding_adjustment_declaration'] = enums.CorrespondingAdjustmentDeclaration.Unknown.name
                df.loc[index, 'corresponding_adjustment_status'] = enums.CorrespondingAdjustmentStatus.NotStarted.name
        except KeyError as e:
            print(f"Error updating corresponding_adjustment: {e}")
        try:
            cmhq_project_id = projects_mapping.get(row['project_id'])
            if not cmhq_project_id:
                raise Exception(f"No project found for project {row['project_id']}")
            
            issuance = issuance_sheet[
                (issuance_sheet['cmhq_project_id'] == cmhq_project_id) &
                (issuance_sheet['vintage_year'] == row['vintage_year'])    
            ]
            if issuance.empty:
                raise Exception(f"Issuance not found for project {cmhq_project_id} & {row['vintage_year']}")
            
            issuance_id = issuance['issuance_id'].values[0]
            print(f"Found issuance {issuance_id} for project {cmhq_project_id}")
            df.loc[index, 'issuance_id'] = issuance_id

        except Exception as e:
            print(f"Error fetching related issuance: {e}")
            continue

        try:
            if os.path.exists(labels_file_path):
                labels = pd.read_csv(labels_file_path)
                label = labels[labels['cmhq_project_id'] == cmhq_project_id]
                if not label.empty:
                    df.loc[index, 'label_id'] = label['label_id'].values[0]
        except Exception as e:
            print(f"Error fetching related Label: {e}")

        if "Protocol Version" in row:
            if row["Protocol Version"]:
                methodology = utils.car_map_methodology_enum(row["Protocol Version"])
                if methodology:
                    projects_sheet.loc[projects_sheet['cmhq_project_id'] == cmhq_project_id, "methodology"] = methodology
                    print(f"Updated methodology for project {cmhq_project_id} to {methodology}")
        
        unit_tags = {}

        for k, v in constants.car_unit_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                unit_tags.update({k: row[k]})
        
        df.loc[index, 'unit_tags'] = json.dumps(unit_tags)
        records.append(df.loc[index].to_dict())

    # update projects
    utils.direct_merge_and_update_csv(projects_sheet, 
                                      projects_file_path)

    if records:
        df_cleaned = pd.DataFrame(records)
        df_cleaned = df_cleaned.where(pd.notnull(df_cleaned), None)
        df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
            lambda row: utils.generate_uuid_from_row(row, ['Offset Credit Serial Numbers', 'project_id', 'issuance_id', 'unit_status', 'unit_status_time', 'unit_count']),
            axis=1
        )
        existing_columns = [col for col in schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        target_csv_path = os.path.join(data_dir, table_name + ".csv")
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {table_name}.csv.")
