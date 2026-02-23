#!/bin/bash
# Standalone SonarQube installation script (runs via Docker)
export DEBIAN_FRONTEND=noninteractive

sudo apt update -y
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker

sudo docker run -d --name sonarqube --restart unless-stopped \
  -p 9000:9000 \
  -v sonarqube_data:/opt/sonarqube/data \
  sonarqube:community
