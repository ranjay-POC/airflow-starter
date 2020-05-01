"""
@author: ranjayd
"""
from airflow import DAG
from airflow import AirflowException
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import date, timedelta, datetime 
from collections import OrderedDict
from airflow.hooks.mysql_hook import MySqlHook
from airflow.hooks.hive_hooks import BaseHook
import os 
from airflow.operators.mssql_operator import MsSqlOperator
import pyodbc
import pandas as pd
from airflow import AirflowException
from scripts.loader_utils import LoaderUtils
from airflow.operators.sensors import BaseSensorOperator


class ManualInterventionSensor(BaseSensorOperator): 

    def __init__(self, *args, **kwargs): 
        super(ManualInterventionSensor, self).__init__(*args, **kwargs)

    def poke(self, context):
        lc = LoaderUtils()
        if lc.get_stat1_status() == 'Y':
            print("Wow... Sensor status is Good to go")
            return True
        else:
            print("Well, Not ready to continue the tasks in the pipeline, waiting for the user to check some status")
            return False
     

default_args = {
    "owner": "Airflow",
    "depends_on_past": True,
    "max_active_runs": 1,
    "start_date": datetime(2015, 6, 1),
    "is_active": True,
    "is_paused_upon_creation": False,
}


def begin_pipeline(**kwargs): 
    print("begin_pipeline()")
    
    
def reset_stat1_status(**kwargs):
    print("reset_stat1_status()")
    lc = LoaderUtils()
    lc.reset_stat1_status()


def download_file(**kwargs): 
    print("download_file()")
    lc = LoaderUtils()
    directory, working_dir = lc.create_working_dir()  
    file1 = 'file1.csv'
    file_path = directory + "/" + file1
    downloaded_file = lc.download_file(file1, file_path)
    kwargs["ti"].xcom_push(key="file_to_load", value=downloaded_file)
    kwargs["ti"].xcom_push(key="temp_directory", value=directory)

 
def load_file(**kwargs): 
    print("load_file()") 
    file_to_load = kwargs["ti"].xcom_pull(key="file_to_load") 
    lc = LoaderUtils()
    lc.load_file1(file_to_load)

 
def cleanup(**kwargs):
    print("cleanup()") 
    temp_directory = kwargs["ti"].xcom_pull(key="temp_directory") 
    lc = LoaderUtils()
    lc.cleanup_directory(temp_directory)

            
def end(**kwargs):
    print("end") 


dag = DAG(
    "s3file_manual_intervention_database",
    description="Pull file from s3 and wait for manual input then load into database",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    orientation="TB",
)

t_sensor_task = ManualInterventionSensor(task_id='manual_intervention', poke_interval=10, dag=dag)

t_pipeline_begin = PythonOperator(
    task_id="begin_pipeline",
    python_callable=begin_pipeline,
    provide_context=True,
    dag=dag,
)

t_reset_stat1_status = PythonOperator(
    task_id="reset_stat1_status",
    python_callable=reset_stat1_status,
    provide_context=True,
    dag=dag,
)

t_download_file = PythonOperator(
    task_id="download_file",
    python_callable=download_file,
    provide_context=True,
    dag=dag,
)

t_load_file = PythonOperator(
    task_id="load_file",
    python_callable=load_file,
    provide_context=True,
    dag=dag,
)
  
t_cleanup = PythonOperator(
    task_id="cleanup",
    python_callable=cleanup,
    provide_context=True,
    dag=dag,
)

t_end = PythonOperator(
    task_id="end",
    python_callable=end,
    provide_context=True,
    dag=dag,
)

t_pipeline_begin >> t_reset_stat1_status >> t_download_file >> t_sensor_task >> t_load_file >> t_cleanup >> t_end
