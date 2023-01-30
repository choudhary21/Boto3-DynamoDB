from flask import request, jsonify
from src.config import *
from http import HTTPStatus
import boto3
from .constants import *
from flask import current_app
import time


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

        # Checking if PITR is already enabled
        pitr_response = client.describe_continuous_backups(
            TableName= table
            )
        isEnabled = pitr_response["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]["PointInTimeRecoveryStatus"]
        if isEnabled == "ENABLED":
            return jsonify({"message" : PITR_ALREADY_ENABALED}), HTTPStatus.OK
        # print("pitr: ", pitr_response["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]["PointInTimeRecoveryStatus"])
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

        return jsonify({"message" : TABLE_EXPORTED}), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST


# Function for listing all the exports
def listExports():
    data = []
    try:
        bucket = request.get_json()["bucket"]
        # maxRes = request.get_json()["Max"]
        current_app.logger.info("Creating client instance for listing all exported files")
        client = boto3.resource(
            's3', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY,
            region_name = REGION
            )
        response = client.Bucket(bucket)
        summaries = response.objects.all()
        print("files", summaries)
        if summaries == None: # condition if we get none response
            raise Exception(NONE_VALUE)
        for files in summaries:
            # print("data: ", files)
            if(files.key[-5:] == ".json"):
                data.append(files.key)
        return jsonify(data), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST
        
    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

# Function for listing all tables of DynamoDB
def listTables():
    try:
        # tableName = request.get_json()["TableName"]
        limit = request.get_json()["Limit"]
        current_app.logger.info("Creating client instance for listing all tables")
        client = boto3.client(
            'dynamodb', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )

        tableResponse = client.list_tables(Limit = limit)

        sqsClient =  boto3.client(
            'sqs', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
        ) 
        
        for table in tableResponse["TableNames"]:
            sqsResponse = sqsClient.send_message(
                QueueUrl = "arn:aws:sqs:us-east-1:300023816116:test",
                MessageBody = table
            )
            
        return jsonify(tableResponse["TableNames"]), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

# Function for pushing messages in SQS queue
def pushMessages():
    try:
        url = request.get_json()["queueUrl"]
        message = request.get_json()["MessageBody"]
        current_app.logger.info("Creating client instance for sending messages to SQS queur")
        client = boto3.client(
            'sqs', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
        )
        response = client.send_message(
            QueueUrl=url,
            MessageBody=message
        )
        # print(response)
        return response
        # return jsonify({"message" : MESSAGE_PUSHED}), HTTPStatus.OK

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST


# bucket = "my-demo1"
# client = boto3.client('dynamodb')
# response = client.export_table_to_point_in_time(
#             TableArn = 
#             f"arn:aws:dynamodb:us-east-1:300023816116:table/{table_name_from_event}",
#             S3Bucket = bucket,
#             ExportFormat="DYNAMODB_JSON"
#         )