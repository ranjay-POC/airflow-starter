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
  
  
def build_file(**kwargs): 
    print("build_file()")
    lc = LoaderUtils()
    directory, working_dir = lc.create_working_dir()  
    file_name = 'file1.csv'
    file_path = directory + "/" + file_name
    upload_file = lc.build_file1(file_name, file_path)
    kwargs["ti"].xcom_push(key="file_to_upload", value=upload_file)
    kwargs["ti"].xcom_push(key="temp_directory", value=directory) 
    kwargs["ti"].xcom_push(key="working_dir", value=working_dir)
    kwargs["ti"].xcom_push(key="file_name", value=file_name)    

    
def transfer_file(**kwargs): 
    print("transfer_file()") 
    file_to_upload = kwargs["ti"].xcom_pull(key="file_to_upload")  
    working_dir = kwargs["ti"].xcom_pull(key="working_dir")  
    file_name = kwargs["ti"].xcom_pull(key="file_name")  
    lc = LoaderUtils()
    lc.upload_file_to_s3(working_dir, file_to_upload, file_name)   
     
        
def cleanup(**kwargs):
    print("cleanup()") 
    temp_directory = kwargs["ti"].xcom_pull(key="temp_directory") 
    lc = LoaderUtils()
    lc.cleanup_directory(temp_directory)     

            
def end(**kwargs):
    print("end") 


dag = DAG(
    "database_to_s3",
    description="Read table from Database, build CSV, upload to S3",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    orientation="TB",
)

t_pipeline_begin = PythonOperator(
    task_id="begin_pipeline",
    python_callable=begin_pipeline,
    provide_context=True,
    dag=dag,
)

t_build_file = PythonOperator(
    task_id="build_file",
    python_callable=build_file,
    provide_context=True,
    dag=dag,
)

t_transfer_file = PythonOperator(
    task_id="transfer_file",
    python_callable=transfer_file,
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

t_pipeline_begin >> t_build_file >> t_transfer_file >> t_cleanup >> t_end
