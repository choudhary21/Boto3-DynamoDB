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
        current_app.logger.info("Creating client instance for updatinf PITR")
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

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

# function to export tables to S3
def exportToS3():
    try:
        arn = request.get_json()["TableArn"]
        bucket = request.get_json()["S3Bucket"]
        current_app.logger.info("Creating client instance for exporting to s3")
        client = boto3.client(
            'dynamodb', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )

        response = client.export_table_to_point_in_time(
            TableArn = arn,
            S3Bucket = bucket,
            ExportFormat="DYNAMODB_JSON"
        )
        current_app.logger.info("Sending successful response after exporting table")
        return jsonify({"message" : TABLE_EXPORTED}), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST


# Function for listing all the exports
def listExports():
    try:
        arn = request.get_json()["TableArn"]
        maxRes = request.get_json()["Max"]
        current_app.logger.info("Creating client instance for listing all exported files")
        client = boto3.client(
            'dynamodb', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )
        response = client.list_exports(
            TableArn = arn,
            MaxResults = maxRes
        )
        return jsonify(response), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST
        
    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST