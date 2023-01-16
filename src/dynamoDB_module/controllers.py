from flask import request, jsonify
from src.config import *
from http import HTTPStatus
import boto3
from .constants import *
from flask import current_app


# function for enabling the PITR for a table of DynamoDB
def update_PITR():
    try:
        table = request.get_json()['table']
        current_app.logger.info("Creating client instance for DynamoDB")
        client = boto3.client(
            'dynamodb', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )
        current_app.logger.info("Sending request to enable PITR")
        response = client.update_continuous_backups(
            TableName = table,
            PointInTimeRecoverySpecification={
                'PointInTimeRecoveryEnabled': True
            }
        )
        # print("res",response)
        current_app.logger.info("Sending successful response after enabling the PITR")
        return jsonify({"message" : PITR_ENABALED}), HTTPStatus.OK

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, 