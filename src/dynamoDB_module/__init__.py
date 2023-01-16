from flask import Blueprint
from .controllers import *


dynamoDB = Blueprint('dynamoDB', __name__, url_prefix = '/api/dynamodb')

# route for enebling Point-In-Time-Restore
dynamoDB.add_url_rule('/PITR', 'update_PITR', update_PITR, methods = ['PATCH'])