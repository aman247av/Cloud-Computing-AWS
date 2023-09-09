#!/bin/bash
sudo yum update -y

sudo su -
dnf -y localinstall https://dev.mysql.com/get/mysql80-community-release-el9-4.noarch.rpm
dnf -y install mysql mysql-community-client mysql-community-server

sudo yum install python3 -y
sudo yum install python3-pip -y
sudo pip3 install Flask
sudo pip3 install pymysql



sudo systemctl start mysqld
sudo systemctl enable mysqld



aws configure set aws_access_key_id $aws_access_key_id
aws configure set aws_secret_access_key $aws_secret_access_key
aws configure set default.region ap-south-1

aws s3 cp s3://lab5-flask-website / --recursive





# 
# mysql -h mysql-db-instance-lab5.co0ynpevyflj.ap-south-1.rds.amazonaws.com -P 3306 -u admin -p