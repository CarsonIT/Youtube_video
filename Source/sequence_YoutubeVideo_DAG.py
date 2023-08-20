from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow import DAG
import datetime


dag = DAG(
    dag_id="sequence_YoutubeVideo_DAG",
    start_date=datetime.datetime(2023, 8, 19),
    catchup=False,
    tags=["Youtube_video_pipeline"],
    schedule_interval=None,
)

# Task call DAG, 
video_DAG = TriggerDagRunOperator(
    task_id="video_DAG",
    trigger_dag_id="video_DAG",  # Ensure this equals the dag_id of the DAG to trigger
    dag=dag,
    )

# Task call DAG, 
category_and_country_DAG = TriggerDagRunOperator(
    task_id="category_and_country_DAG",
    trigger_dag_id="category_and_country_DAG",  # Ensure this equals the dag_id of the DAG to trigger
    dag=dag,
    )

category_and_country_DAG >> video_DAG
