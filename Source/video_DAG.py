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
    dag_id="video_DAG",
    start_date=datetime.datetime(2023, 8, 17),
    catchup=False,
    tags=["Youtube_video_pipeline"],
    schedule_interval=None,
)

def extract_all_file_csv():
    try:
        # Read file all video csv
        us_csv_file_path = '/home/ubuntu/Documents/USvideos.csv'
        gb_csv_file_path = '/home/ubuntu/Documents/GBvideos.csv'
        in_csv_file_path = '/home/ubuntu/Documents/INvideos.csv'
        de_csv_file_path = '/home/ubuntu/Documents/DEvideos.csv'
        ca_csv_file_path = '/home/ubuntu/Documents/CAvideos.csv'
        fr_csv_file_path = '/home/ubuntu/Documents/FRvideos.csv'
        kr_csv_file_path = '/home/ubuntu/Documents/KRvideos.csv'
        ru_csv_file_path = '/home/ubuntu/Documents/RUvideos.csv'
        jp_csv_file_path = '/home/ubuntu/Documents/JPvideos.csv'
        mx_csv_file_path = '/home/ubuntu/Documents/MXvideos.csv'

        # Read all file csv
        us_df = pd.read_csv(us_csv_file_path)
        gb_df = pd.read_csv(gb_csv_file_path)
        in_df = pd.read_csv(in_csv_file_path)
        de_df = pd.read_csv(de_csv_file_path)
        ca_df = pd.read_csv(ca_csv_file_path)
        fr_df = pd.read_csv(fr_csv_file_path)
        kr_df = pd.read_csv(kr_csv_file_path,encoding='latin-1')
        ru_df = pd.read_csv(ru_csv_file_path,encoding='latin-1')
        jp_df = pd.read_csv(jp_csv_file_path,encoding='latin-1')
        mx_df = pd.read_csv(mx_csv_file_path,encoding='latin-1')

        # Select colummn
        columns_to_select = ['video_id', 'trending_date', 'title', 'channel_title','category_id','publish_time','views','likes','dislikes','comment_count']
        
        # Create new dataframe
        us_df_new = us_df[columns_to_select]
        gb_df_new = gb_df[columns_to_select]
        in_df_new = in_df[columns_to_select]
        de_df_new = de_df[columns_to_select]
        ca_df_new = ca_df[columns_to_select]
        fr_df_new = fr_df[columns_to_select]
        kr_df_new = kr_df[columns_to_select]
        ru_df_new = ru_df[columns_to_select]
        jp_df_new = jp_df[columns_to_select]
        mx_df_new = mx_df[columns_to_select]

        # Add column country_id
        us_df_new['country_id'] = 1
        gb_df_new['country_id'] = 2
        in_df_new['country_id'] = 3
        de_df_new['country_id'] = 4
        ca_df_new['country_id'] = 5
        fr_df_new['country_id'] = 6
        kr_df_new['country_id'] = 7
        ru_df_new['country_id'] = 8
        jp_df_new['country_id'] = 9
        mx_df_new['country_id'] = 10
        
        # Create new csv file in folder staging
        staging_us_csv_file = '/home/ubuntu/Documents/staging/US_staging_videos.csv'
        staging_gb_csv_file = '/home/ubuntu/Documents/staging/GB_staging_videos.csv'
        staging_in_csv_file = '/home/ubuntu/Documents/staging/IN_staging_videos.csv'
        staging_de_csv_file = '/home/ubuntu/Documents/staging/DE_staging_videos.csv'
        staging_ca_csv_file = '/home/ubuntu/Documents/staging/CA_staging_videos.csv'
        staging_fr_csv_file = '/home/ubuntu/Documents/staging/FR_staging_videos.csv'
        staging_kr_csv_file = '/home/ubuntu/Documents/staging/KR_staging_videos.csv'
        staging_ru_csv_file = '/home/ubuntu/Documents/staging/RU_staging_videos.csv'
        staging_jp_csv_file = '/home/ubuntu/Documents/staging/JP_staging_videos.csv'
        staging_mx_csv_file = '/home/ubuntu/Documents/staging/MX_staging_videos.csv'

        #Write data frame to csv
        us_df_new.to_csv(staging_us_csv_file,index=False)
        gb_df_new.to_csv(staging_gb_csv_file,index=False)
        in_df_new.to_csv(staging_in_csv_file,index=False)
        de_df_new.to_csv(staging_de_csv_file,index=False)
        ca_df_new.to_csv(staging_ca_csv_file,index=False)
        fr_df_new.to_csv(staging_fr_csv_file,index=False)
        kr_df_new.to_csv(staging_kr_csv_file,index=False)
        ru_df_new.to_csv(staging_ru_csv_file,index=False)
        jp_df_new.to_csv(staging_jp_csv_file,index=False)
        mx_df_new.to_csv(staging_mx_csv_file,index=False)

    except Exception as e:
        raise ValueError('Email to DataEngineer about error that: ',e)
        return False

def truncate_table_video():
    try:
        #Tạo thông tin connect tới Database 
        hook_target = MsSqlHook(mssql_conn_id="connect_mssql", schema="YoutubeVideo")
        engine_target = hook_target.get_sqlalchemy_engine()
        #Truncate table 
        engine_target.execute(sa_text('''TRUNCATE TABLE Video''').execution_options(autocommit=True))
    except Exception as e:
        raise ValueError('Email to DataEngineer about error that: ',e)
        return False

def transform_load_all_csv_to_db():
    try:
        # read all csv files starting with "df"
        df = dd.read_csv("/home/ubuntu/Documents/staging/*_staging_videos.csv")
        df = df.compute()
        
        # Chuyển đổi cột 'trending_date' sang kiểu dữ liệu date
        df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')
        # Chuyển đổi cột 'publish_time' sang kiểu dữ liệu datetime
        df['publish_time'] = pd.to_datetime(df['publish_time'])
        #Tạo thông tin connect tới Database 
        hook_target = MsSqlHook(mssql_conn_id="connect_mssql", schema="YoutubeVideo")
        engine_target = hook_target.get_sqlalchemy_engine()

        df.to_sql('Video', engine_target, if_exists='append', index=False,
        dtype = {
       'video_id':  sqlalchemy.types.VARCHAR(length=11),
       'trending_date': sqlalchemy.types.DATE(),
       'title':  sqlalchemy.types.NVARCHAR(length=200),
       'channel_title':  sqlalchemy.types.NVARCHAR(length=300),
       'category_id': sqlalchemy.types.INTEGER(),
       'publish_time': sqlalchemy.types.DATETIME(),
       'views': sqlalchemy.types.INTEGER(),
       'likes': sqlalchemy.types.INTEGER(),
       'dislikes': sqlalchemy.types.INTEGER(),
       'comment_count': sqlalchemy.types.INTEGER(),
       'country_id': sqlalchemy.types.INTEGER()})

        print("Data load into target database successfully")

    except Exception as e:
        raise ValueError('Email to DataEngineer about error that: ',e)
        return False

extract_all_file_csv = PythonOperator(
    task_id="extract_all_file_csv",
    python_callable=extract_all_file_csv,
    dag=dag,
    )

transform_load_all_csv_to_db = PythonOperator(
    task_id="transform_load_all_csv_to_db",
    python_callable=transform_load_all_csv_to_db,
    dag=dag,
    )    

truncate_table_video = PythonOperator(
    task_id="truncate_table_video",
    python_callable=truncate_table_video,
    dag=dag,
    )  

extract_all_file_csv >> truncate_table_video >> transform_load_all_csv_to_db