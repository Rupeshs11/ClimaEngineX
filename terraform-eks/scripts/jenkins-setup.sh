#!/bin/bash
# Standalone Jenkins installation script
export DEBIAN_FRONTEND=noninteractive

sudo apt update -y
sudo apt install fontconfig openjdk-21-jre -y

sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update -y
sudo apt-get install jenkins -y
sudo systemctl enable jenkins
sudo systemctl start jenkins

# Install Docker for Jenkins
sudo apt install docker.io -y
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
