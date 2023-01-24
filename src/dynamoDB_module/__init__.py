from flask import Blueprint
from .controllers import *


dynamoDB = Blueprint('dynamoDB', __name__, url_prefix = '/api/dynamodb')

# route for enebling Point-In-Time-Restore
dynamoDB.add_url_rule('/PITR', 'update_PITR', update_PITR, methods = ['PATCH'])

# route for exporting table to s3
dynamoDB.add_url_rule('/export', 'exportToS3', exportToS3, methods = ['PATCH'])

# route for listing all tables 
dynamoDB.add_url_rule('/list', 'listTables', listTables, methods = ['GET'])

# route for listing all export files(JSON)
dynamoDB.add_url_rule('/listExport', 'listExports', listExports, methods = ['GET'])

# route for sending message to SQS 
# dynamoDB.add_url_rule('/pushtosqs', 'sendSQS', sendSQS, methods = ['GET'])

# route for recieving message to SQS 
# dynamoDB.add_url_rule('/recievedtosqs', 'recieveSQS', recieveSQS, methods = ['GET'])