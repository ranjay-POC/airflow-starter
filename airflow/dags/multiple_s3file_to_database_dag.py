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


def prepare_files(**kwargs): 
    print("prepare_files()")
    lc = LoaderUtils()
    directory, working_dir = lc.create_working_dir() 
    file1 = 'file1.csv'
    file_path1 = directory + "/" + file1 
    file2 = 'file2.csv'
    file_path2 = directory + "/" + file2 
     
    kwargs["ti"].xcom_push(key="file1", value=file1)
    kwargs["ti"].xcom_push(key="file_path1", value=file_path1)
    kwargs["ti"].xcom_push(key="file2", value=file2)
    kwargs["ti"].xcom_push(key="file_path2", value=file_path2)
    kwargs["ti"].xcom_push(key="temp_directory", value=directory) 
    kwargs["ti"].xcom_push(key="working_dir", value=working_dir)  

    
def download_file1(**kwargs): 
    print("download_file1()")
    lc = LoaderUtils()
    downloaded_file = lc.download_file(kwargs["ti"].xcom_pull(key="file1"), kwargs["ti"].xcom_pull(key="file_path1"))
    kwargs["ti"].xcom_push(key="file1_to_load", value=downloaded_file)
    
def download_file2(**kwargs): 
    print("download_file2()") 
    lc = LoaderUtils()
    downloaded_file = lc.download_file(kwargs["ti"].xcom_pull(key="file2"), kwargs["ti"].xcom_pull(key="file_path2"))
    kwargs["ti"].xcom_push(key="file2_to_load", value=downloaded_file)       
 

def validate_files(**kwargs): 
    print("validate_files()")

    
def load_file1(**kwargs): 
    print("load_file1()") 
    file_to_load = kwargs["ti"].xcom_pull(key="file1_to_load") 
    lc = LoaderUtils()
    lc.load_file1(file_to_load)    

    
def load_file2(**kwargs): 
    print("load_file2()") 
    file_to_load = kwargs["ti"].xcom_pull(key="file2_to_load") 
    lc = LoaderUtils()
    lc.load_file2(file_to_load)     


def cleanup(**kwargs):
    print("cleanup()") 
    temp_directory = kwargs["ti"].xcom_pull(key="temp_directory") 
    lc = LoaderUtils()
    lc.cleanup_directory(temp_directory)    

            
def end(**kwargs):
    print("end") 


dag = DAG(
    "multiple_s3files_to_database",
    description="Pull multiple files from s3 and load into database",
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

t_prepare_files = PythonOperator(
    task_id="prepare_files",
    python_callable=prepare_files,
    provide_context=True,
    dag=dag,
)

t_download_file1 = PythonOperator(
    task_id="download_file1",
    python_callable=download_file1,
    provide_context=True,
    dag=dag,
)

t_download_file2 = PythonOperator(
    task_id="download_file2",
    python_callable=download_file2,
    provide_context=True,
    dag=dag,
)
  

t_validate_files = PythonOperator(
    task_id="validate_files",
    python_callable=validate_files,
    provide_context=True,
    dag=dag,
)

t_load_file1 = PythonOperator(
    task_id="load_file1",
    python_callable=load_file1,
    provide_context=True,
    dag=dag,
)


t_load_file2 = PythonOperator(
    task_id="load_file2",
    python_callable=load_file2,
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

t_pipeline_begin >> t_prepare_files 
t_prepare_files >> [ t_download_file1, t_download_file2 ] >> t_validate_files >> [ t_load_file1, t_load_file2 ] >> t_cleanup >> t_end

