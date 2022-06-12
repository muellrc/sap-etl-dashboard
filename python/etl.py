# Imports

from pyodata.v2.model import Config
import pyodata
import requests
import pandas as pd
import json
from prefect import task, Flow
from prefect.schedules import IntervalSchedule
from prefect.executors import LocalDaskExecutor
from sqlalchemy import create_engine

# Local imports from this folder
import dbconfig 
import sapconfig

@task
def extract_equipment():
    ''''
    Task to extract the source data 
    '''
    # Read source data

    SERVICE_URL = sapconfig.sap_gateway_url + sapconfig.get_equipment_service

    session = requests.Session()
    param = {'sap-client': sapconfig.sap_client}

    session.auth = (sapconfig.gateway_username,sapconfig.gateway_password)

    svc_getequipment = pyodata.Client(SERVICE_URL, session)

    EquipmentListSet = getattr(
            svc_getequipment.entity_sets, sapconfig.get_equipment_entity).get_entities()

    EquipmentListSet = EquipmentListSet.filter(sapconfig.get_equipment_filter)

    equipments = []
    for EquipmentList in EquipmentListSet.execute():
        all_vars = EquipmentList._cache
        all_vars_dict = json.loads(json.dumps(all_vars))
        equipments.append(all_vars_dict)
        
    equipment_data = pd.DataFrame(equipments)
    print(equipment_data) 
    # Return data from source
    return equipment_data

@task
def transform_equipment(equipment_data):
    ''''
    Task to transform the source data
    '''
    #Placeholder for transformations with the received dataframe

    # Return transformed data
    return equipment_data

@task
def load_equipment(equipment_data):
    ''''
    Task to load the processed data into the database
    '''
    engine = create_engine('postgresql://' + dbconfig.USER + ':' + dbconfig.PASSWORD + '@' + dbconfig.HOST + ':5432/' + dbconfig.DBNAME)

    equipment_data.to_sql("equipment", engine, if_exists='replace')

    return "--- Process successfully completed! ---"


@task
def extract_funcloc():
    ''''
    Task to extract the source data 
    '''
    # Read source data

    SERVICE_URL = sapconfig.sap_gateway_url + sapconfig.get_funcloc_service

    session = requests.Session()
    param = {'sap-client': sapconfig.sap_client}

    session.auth = (sapconfig.gateway_username,sapconfig.gateway_password)

    svc_getfuncloc = pyodata.Client(SERVICE_URL, session)

    FuncLocListSet = getattr(
            svc_getfuncloc.entity_sets, sapconfig.get_funcloc_entity).get_entities()

    FuncLocListSet = FuncLocListSet.filter(sapconfig.get_funcloc_filter)

    funclocs = []
    for FuncLocList in FuncLocListSet.execute():
        all_vars = FuncLocList._cache
        all_vars_dict = json.loads(json.dumps(all_vars))
        funclocs.append(all_vars_dict)
        
    funcloc_data = pd.DataFrame(funclocs)
    print(funcloc_data) 
    # Return data from source
    return funcloc_data

@task
def transform_funcloc(funcloc_data):
    ''''
    Task to transform the source data
    '''
    #Placeholder for transformations with the received dataframe

    # Return transformed data
    return funcloc_data

@task
def load_funcloc(funcloc_data):
    ''''
    Task to load the processed data into the database
    '''
    engine = create_engine('postgresql://' + dbconfig.USER + ':' + dbconfig.PASSWORD + '@' + dbconfig.HOST + ':5432/' + dbconfig.DBNAME)

    funcloc_data.to_sql("funcloc", engine, if_exists='replace')

    return "--- Process successfully completed! ---"

def main():
    '''
    Set Prefect flow and execute schedule
    '''

    # Configure Prefect flow
    with Flow("etl") as flow:

        #Equipment
        equipment_data = extract_equipment()
        equipment_data = transform_equipment(equipment_data)
        load_equipment(equipment_data)

        #Functional Location
        funcloc_data = extract_funcloc()
        funcloc_data = transform_funcloc(funcloc_data)
        load_funcloc(funcloc_data)

    # Execute ETL flow
    flow.run(executor=LocalDaskExecutor())

if __name__ == "__main__":
    main()
