from flask import Blueprint
from .controllers import *


dynamoDB = Blueprint('dynamoDB', __name__, url_prefix = '/api/dynamodb')

# route for enebling Point-In-Time-Restore
dynamoDB.add_url_rule('/PITR', 'update_PITR', update_PITR, methods = ['PATCH'])

# route for exporting table to s3
dynamoDB.add_url_rule('/export', 'exportToS3', exportToS3, methods = ['PATCH'])

# route for listing all exported files
dynamoDB.add_url_rule('/listexports', 'listExports', listExports, methods = ['GET', 'POST'])


dynamoDB.add_url_rule('/listtables', 'listTables', listTables)


dynamoDB.add_url_rule('/pushmessage', 'pushMessages', pushMessages)

dynamoDB.add_url_rule('/getPitr', 'getPitr', getPitr, methods = ['GET', 'POST'])
