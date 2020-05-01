#!/usr/bin/env bash

echo "Remove all containers"
docker  ps -as

docker stop airflow
docker rm airflow

docker stop postgres
docker rm postgres

docker stop mssql_database
docker rm mssql_database

docker stop jenkins
docker rm jenkins


sleep 2

docker  ps -as
