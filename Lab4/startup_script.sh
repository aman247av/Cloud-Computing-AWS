#!/bin/bash 
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
yum update -y
yum install -y httpd



systemctl start httpd
systemctl enable httpd

aws configure set aws_access_key_id $aws_access_key_id
aws configure set aws_secret_access_key $aws_secret_access_key
aws configure set default.region ap-south-1

aws s3 cp s3://lab1-part2-pw/Website/ /var/www/html/ --recursive

chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html

curl localhost:80
systemctl restart httpd
