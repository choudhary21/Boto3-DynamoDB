import boto3
from src.config import *

def create_client(module):
    client = boto3.client(
            module, 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )
    return client

def create_resource(module):
    resource = boto3.resource(
        module,
        aws_access_key_id = ACCESS_KEY, 
        aws_secret_access_key = SECRET_KEY, 
        region_name = REGION
    )
    return resource