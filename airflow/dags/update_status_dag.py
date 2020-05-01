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

    
def update_status(**kwargs): 
    print("update_status()") 
    lc = LoaderUtils()
    lc.update_status()      


def cleanup(**kwargs):
    print("cleanup()") 

            
def end(**kwargs):
    print("end") 


dag = DAG(
    "update_status",
    description="Update True status in database to simulate manual intervention",
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

t_update_status = PythonOperator(
    task_id="update_status",
    python_callable=update_status,
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

t_pipeline_begin >> t_update_status >> t_cleanup >> t_end

