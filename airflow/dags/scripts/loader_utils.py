"""
@author: ranjayd
"""

import pyodbc
import csv
import os
import boto3
from datetime import datetime
import shutil
import random
import string
from airflow.exceptions import AirflowException


class LoaderUtils: 

    def get_connection(self):
        server = os.environ.get("MSSQL_HOST", None)
        database = os.environ.get("MSSQL_DATABASE", None)
        username = os.environ.get("MSSQL_USERNAME", None)
        password = os.environ.get("MSSQL_PASSWORD", None)
        connection = pyodbc.connect('DRIVER='+os.environ.get("MSSQL_DRIVER", None) +';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        return connection    
    
    def get_s3_client(self):
        return boto3.client(
            "s3", aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", None), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", None), region_name=os.environ.get("AWS_REGION_NAME", "us-east-1")
        )    
    
    def build_file1(self, file_name, file_path):
        print("Reading data from file1 table and building csv file [{0}] and file location [{1}]".format(file_name, file_path))
        conn = self.get_connection() 
        cursor = conn.cursor() 
        cursor.execute("select id, name from loaderdb.dbo.file1")
         
        with open(file_path, mode='w') as csv_file:
            fieldnames = ['id', 'name'] 
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)  
            writer.writerow(fieldnames)  
            for row in cursor:
                writer.writerow([row[0], row[1]])  
                
        return file_path
                
    def upload_file_to_s3(self, working_dir, file_to_upload, file_name):
        print("Uploading file [{0}] to S3".format(file_to_upload))
        client = self.get_s3_client()
        data = open(file_to_upload, 'rb') 
        client.put_object(Bucket=os.environ.get("AWS_S3_BUCKET", None), Key=('outbound/' + working_dir + '/' + file_name), Body=data)                              
         
    def load_file1(self, file):  
        print("load_file1: file [{0}]".format(file))
        reader = csv.DictReader(open(file)) 
        conn = self.get_connection() 
        cursor = conn.cursor()   
        
        # delete and load data 
        cursor.execute("delete from loaderdb.dbo.file1")
        print('Deleted {0} records: '.format(str(cursor.rowcount)))
        conn.commit() 
        
        cursor = conn.cursor()
        for raw in reader:
            cursor.execute("insert into loaderdb.dbo.file1(name) values (?)", raw['name'])
        cursor.commit() 
        
        # count
        cursor.execute('select count(*) as "count" from loaderdb.dbo.file1')
        row = cursor.fetchone()
        print('Loaded {0} records'.format(row[0])) 
        
    def load_file2(self, file):  
        print("load_file2: file [{0}]".format(file))
        reader = csv.DictReader(open(file)) 
        conn = self.get_connection() 
        cursor = conn.cursor()   
        
        # delete and load data 
        cursor.execute("delete from loaderdb.dbo.file2")
        print('Deleted {0} records: '.format(str(cursor.rowcount)))
        conn.commit() 
        
        cursor = conn.cursor()
        for raw in reader:
            cursor.execute("insert into loaderdb.dbo.file2(name) values (?)", raw['name'])
        cursor.commit() 
        
        # count
        cursor.execute('select count(*) as "count" from loaderdb.dbo.file2')
        row = cursor.fetchone()
        print('Loaded {0} records'.format(row[0]))                
        
    def download_file(self, file_name, file_path): 
        print("Downloading file  [{0}] and file path is [{1}]".format(file_name, file_path))
        client = self.get_s3_client()
        client.download_file(
            os.environ.get("AWS_S3_BUCKET", None), "inbound/" + file_name, file_path
        ) 
        return file_path 
    
    def check_file_size(self, file_name, file_path):
        return 100
    
    def download_file_with_checks(self, file_name, file_path): 
        print("Downloading file  [{0}] and file path is [{1}]".format(file_name, file_path))
        
        file_size = 10
        
        client = self.get_s3_client()
        client.download_file(
            os.environ.get("AWS_S3_BUCKET", None), "inbound/" + file_name, file_path
        ) 
        
        if file_size == self.check_file_size(file_name, file_path):
            return file_path
        else:
            raise AirflowException("Detected download file size is not same as the computed file size, download again or rerun task")
        return file_path     
    
    def cleanup_directory(self, directory):   
        print("Deleting directory [{0}]".format(directory))  
        shutil.rmtree(directory)
        
    def create_working_dir(self): 
        parent_dir = os.getcwd() + "/dags/data"
        mode = 0o777
        working_dir = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") 
        path = os.path.join(parent_dir, working_dir)  
        os.mkdir(path, mode, dir_fd=None)        
        return path, working_dir  
    
    def get_stat1_status(self): 
        print("get_stat1_status()") 
        conn = self.get_connection() 
        cursor = conn.cursor()    
        cursor.execute('select id, name, status as "count" from loaderdb.dbo.sensor_status')
        row = cursor.fetchone() 
        return row[2]
    
    def reset_stat1_status(self): 
        print("reset_stat1_status()") 
        conn = self.get_connection() 
        cursor = conn.cursor()    
        cursor.execute('update loaderdb.dbo.sensor_status set status = \'N\' where name = \'stat1\' ')
        conn.commit() 
    
    def update_status(self): 
        print("update_status()") 
        conn = self.get_connection() 
        cursor = conn.cursor()    
        cursor.execute('update loaderdb.dbo.sensor_status set status = \'Y\' where name = \'stat1\' ')  
        conn.commit()        
    
    
