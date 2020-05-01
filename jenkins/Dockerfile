FROM jenkins/jenkins:lts-jdk11
MAINTAINER Ranjay Kumar <ranjayd@gmail.com>

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

USER root 

RUN apt-get update

RUN curl -fsSL https://get.docker.com | sh

RUN docker --version 

RUN apt-get install jq -y

RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

RUN curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

RUN chmod +x /usr/local/bin/docker-compose

RUN apt-get install awscli -y

RUN apt-get install vim -y


USER root