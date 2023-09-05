import time
import boto3
from config import AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY


session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1'
)

ec2 = session.resource('ec2')

instance = ec2.create_instances(
    ImageId='ami-0ded8326293d3201b',  
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    SecurityGroups=['launch-wizard-1'],  
    UserData=open('startup_script.sh', 'r').read(),
)

instance_id = instance[0].id

instance = ec2.Instance(instance_id)
print('Running and waiting for DNS')
instance.wait_until_running()


public_dns = instance.public_dns_name
print("Public DNS:", public_dns)

