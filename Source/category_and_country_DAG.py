import datetime
from airflow import DAG
import pandas as pd
from airflow.operators.python_operator import PythonOperator
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
import sqlalchemy  
from sqlalchemy.sql import text as sa_text
import os
import dask.dataframe as dd


dag = DAG(
    dag_id="category_and_country_DAG",
    start_date=datetime.datetime(2023, 8, 17),
    catchup=False,
    tags=["Youtube_video_pipeline"],
    schedule_interval=None,
)


def truncate_table_category_video():
    try:
        #Tạo thông tin connect tới Database 
        hook_target = MsSqlHook(mssql_conn_id="connect_mssql", schema="YoutubeVideo")
        engine_target = hook_target.get_sqlalchemy_engine()
        #Truncate table 
        engine_target.execute(sa_text('''TRUNCATE TABLE Category_video''').execution_options(autocommit=True))
    except Exception as e:
        raise ValueError('Email to DataEngineer about error that: ',e)
        return False

def truncate_table_country():
    try:
        #Tạo thông tin connect tới Database 
        hook_target = MsSqlHook(mssql_conn_id="connect_mssql", schema="YoutubeVideo")
        engine_target = hook_target.get_sqlalchemy_engine()
        #Truncate table 
        engine_target.execute(sa_text('''TRUNCATE TABLE Country''').execution_options(autocommit=True))
    except Exception as e:
        raise ValueError('Email to DataEngineer about error that: ',e)
        return False

def extract_category_video_load_db():
    try:
        json_file_path = '/home/ubuntu/Documents/US_category_id.json'
        df_category = pd.read_json(json_file_path)

        rows = []
        for item in df_category['items']:
            row = {
                'kind': df_category['kind'],
                'etag': df_category['etag'],
                'item_kind': item['kind'],
                'item_etag': item['etag'],
                'item_id': item['id'],
                'snippet': item['snippet'],
                'channel_id': item['snippet']['channelId'],
                'title': item['snippet']['title'],
                'assignable': item['snippet']['assignable']
            }
            rows.append(row)

        # Tạo DataFrame từ danh sách dòng dữ liệu
        df_category_temp = pd.DataFrame(rows)

        # Select column
        columns_to_select = ['item_id','title']
        df_category_new = df_category_temp[columns_to_select]

        # Rename column
        df_category_new.rename(columns = {'item_id':'category_id', 'title':'category_name'}, inplace = True)

        # Tạo thông tin connect tới Database 
        hook_target = MsSqlHook(mssql_conn_id="connect_mssql", schema="YoutubeVideo")
        engine_target = hook_target.get_sqlalchemy_engine()

        df_category_new.to_sql('Category_video', engine_target, if_exists='append', index=False,
        dtype = {
       'category_id': sqlalchemy.types.INTEGER(),
       'category_name':  sqlalchemy.types.VARCHAR(length=50)})

        print("Data load into target database successfully")

    except Exception as e:
        raise ValueError('Email to DataEngineer about error that: ',e)
        return False

def extract_country_load_db():
    try:
        # Read file country csv
        country_csv_file_path = '/home/ubuntu/Documents/country/Country.csv'
        df_country = pd.read_csv(country_csv_file_path)

        
        # Tạo thông tin connect tới Database 
        hook_target = MsSqlHook(mssql_conn_id="connect_mssql", schema="YoutubeVideo")
        engine_target = hook_target.get_sqlalchemy_engine()

        df_country.to_sql('Country', engine_target, if_exists='append', index=False,
        dtype = {
       'country_id': sqlalchemy.types.INTEGER(),
       'abbreviation':  sqlalchemy.types.VARCHAR(length=2),
       'country_name':  sqlalchemy.types.VARCHAR(length=60)})

        print("Data load into target database successfully")

    except Exception as e:
        raise ValueError('Email to DataEngineer about error that: ',e)
        return False

truncate_table_category_video = PythonOperator(
    task_id="truncate_table_category_video",
    python_callable=truncate_table_category_video,
    dag=dag,
    )

truncate_table_country = PythonOperator(
    task_id="truncate_table_country",
    python_callable=truncate_table_country,
    dag=dag,
    )    

extract_category_video_load_db = PythonOperator(
    task_id="extract_category_video_load_db",
    python_callable=extract_category_video_load_db,
    dag=dag,
    )  

extract_country_load_db = PythonOperator(
    task_id="extract_country_load_db",
    python_callable=extract_country_load_db,
    dag=dag,
    )  


truncate_table_category_video >> extract_category_video_load_db
truncate_table_country >> extract_country_load_db
