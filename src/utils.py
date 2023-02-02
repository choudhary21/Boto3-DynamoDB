import boto3
from src.config import *

def create_client(resource):
    client = boto3.client(
            resource, 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )