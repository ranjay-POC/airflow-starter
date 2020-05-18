#!/usr/bin/env bash

echo "Install dependencies"

curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

docker-compose --version



sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce
sudo usermod -aG docker $(whoami)
sudo systemctl enable docker.service
sudo systemctl start docker.service


docker info
docker network create airflow-starter
cd ./jenkins
docker-compose down && docker-compose build && docker-compose up -d && sleep 10  &&  docker ps
docker stop jenkins
pwd
ls -altr
cd /opt/airflow-starter/bootstrap_data/jenkins/
cp -R /opt/airflow-starter/bootstrap_data/jenkins/jobs/ /opt/airflow-starter/jenkins/jenkins_home/
cp /opt/airflow-starter/bootstrap_data/jenkins/config.xml /opt/airflow-starter/jenkins/jenkins_home/
docker start jenkins
