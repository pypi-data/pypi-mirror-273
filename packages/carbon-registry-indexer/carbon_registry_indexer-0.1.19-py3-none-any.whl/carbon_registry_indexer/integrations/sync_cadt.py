import os

from carbon_registry_indexer.models import target
from . import utils

import pandas as pd

project_id_mapping = {}

def cadt_projects_upsert(df, data_dir, table_name):
    """
    Process CADT projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    
    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    df.rename(columns={"warehouse_project_id": "cadt_project_id", "description": "project_description"}, inplace=True)
    
    projects_schema = target.Project.__table__.columns.keys()
    existing_columns = [col for col in projects_schema if col in df.columns]
    # remove columns not in schema
    df = df[existing_columns]
    df_cleaned = df.where(pd.notnull(df), None)
    utils.map_enums(table_name, df_cleaned)
    df_cleaned['cmhq_project_id'] = [utils.map_registries_for_id(row['current_registry']) + '-' + str(row['cadt_project_id']) for _, row in df_cleaned.iterrows()]

    for _, row in df_cleaned.iterrows():
        project_id_mapping[row['cadt_project_id']] = row['cmhq_project_id']
    
    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df)} projects. Data saved to {target_csv_path}.")

def cadt_common_upsert(df, data_dir, table_name, schema):
    """
    Process CADT sheets data and save to csv. Generic function to handle multiple tables.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")

    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    if "project_id" in df.columns:
        df.rename(columns={"project_id": "cadt_project_id"}, inplace=True)
        df['cmhq_project_id'] = [project_id_mapping[pid] for pid in df['cadt_project_id']]
    if "cobenefit" in df.columns:
        df.rename(columns={"cobenefit": "co_benefit"}, inplace=True)
        utils.map_cadt_co_benefits(df)

    new_id = f"{utils.camel_to_snake(schema)}_id"
    df.rename(columns={"id": new_id }, inplace=True)

    utils.map_enums(table_name, df)

    for _, row in df.iterrows():
        row['cmhq_project_id'] = project_id_mapping[row['cadt_project_id']]

    schema = getattr(target, schema).__table__.columns.keys()
    existing_columns = [col for col in schema if col in df.columns]
    df = df[existing_columns]

    df_cleaned = df.where(pd.notnull(df), None)

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df)} {table_name}. Data saved to {target_csv_path}.")
 

def cadt_units_upsert(df, data_dir, table_name, issuances_file_name, schema):
    """
    Process CADT units data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    issuances_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    new_id = "cadt_unit_id"
    df.rename(columns={"warehouse_unit_id": new_id }, inplace=True)

    utils.map_enums(table_name, df)

    schema = getattr(target, schema).__table__.columns.keys()
    existing_columns = [col for col in schema if col in df.columns]
    df = df[existing_columns]

    if not os.path.exists(issuances_file_path):
        raise FileNotFoundError(f"Issuances file {issuances_file_path} not found.")
    
    issuances_df = pd.read_csv(issuances_file_path)
    df = df[df['issuance_id'].isin(issuances_df['issuance_id'])]

    df_cleaned = df.where(pd.notnull(df), None)
    df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cadt_unit_id']),
        axis=1
    )
    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df)} units. Data saved to {target_csv_path}.")

def cadt_units_json_handler(all_data, data_dir, table_name, issuances_file_name, schema):
    """
    Process CADT Verra JSON data and save to csv. 
    """
    df = pd.json_normalize(all_data)
    cadt_units_upsert(df, data_dir, table_name, issuances_file_name, schema)
