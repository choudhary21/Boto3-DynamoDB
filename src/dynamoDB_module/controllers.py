from flask import request, jsonify
from src.config import *
from http import HTTPStatus
import boto3
from .constants import *
from flask import current_app
from .service import validate_table
from .service import validate_bucket
# from .service import validate_maxRes

# API for enabling the PITR for a table of DynamoDB
def update_PITR():
    try:
        table = request.get_json()['table']
    # Input validation for Table name in DynamoDB
        validate_table(table) 
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

# API for Export to S3 (json file)

def exportToS3():
    status = False
    try:
        arn = request.get_json()["TableArn"]
        table = request.get_json()["TableName"]
    # Input validation for S3 Table name  
        validate_table(table)
        bucket = request.get_json()["bucket"]
    # Input validation for S3 Bucket name 
        validate_bucket(bucket)
        current_app.logger.info("Creating client instance for exporting to s3")
        client = boto3.client(
            'dynamodb', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )
        table = client.describe_table(
            TableName=table
            )
        table_arn = table['Table']['TableArn']        

        response = client.export_table_to_point_in_time(
            TableArn = table_arn,
            S3Bucket = bucket,
            ExportFormat="DYNAMODB_JSON"
        )

        return response

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

# API for List all the exported json files

def listExports():
    try:
    #     arn = request.get_json()["TableArn"]
    #     maxRes = request.get_json()["Max"]        
    # # Input validation for Maximum results  
    #     validate_maxRes(maxRes)
        current_app.logger.info("Creating client instance for listing all exported files")
        client = boto3.client(
            'dynamodb', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )
        response = client.list_exports(
            # TableArn = arn,
            # MaxResults = maxRes
        )
        return jsonify(response), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST
        
    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

def listTables():
    try:
        # tableName = request.get_json()["TableName"]
        # limit = request.get_json()["Limit"]
        # queueURL = request.get_json()["QueueUrl"]
        # messageBody = request.get_json()["MessageBody"]
        current_app.logger.info("Creating client instance for listing all tables")
        client = boto3.client(
            'dynamodb', 
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )

        response = client.list_tables()  
        # ExclusiveStartTableName = tableName, Limit = limit
        
        # queueURL = request.get_json()["QueueUrl"]
        # messageBody = request.get_json()["MessageBody"]
        # sqsClient = boto3.client(
        #     'sqs',
        #     aws_access_key_id = ACCESS_KEY,
        #     aws_secret_access_key = SECRET_KEY,
        #     region_name = REGION
        # )    

        # for table in response["TableNames"]:
        #     sqsResponse = sqsClient.send_message(
        #         QueueUrl = queueURL,
        #         MessageBody = messageBody
        #     )

        return jsonify(response["TableNames"]), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST


#  "TableName": "Movie",
#     "Limit": 25,
#     "MessageBody": "table",
#     "QueueUrl": "https://sqs.us-east-1.amazonaws.com/300023816116/test"
# def sendSQS():
#     try:
#         queueURL = request.get_json()["QueueUrl"]
#         messageBody = request.get_json()["MessageBody"]
#         # actualMessage = {"message" : messageBody}
#         current_app.logger.info("Creating client to push message on SQS for table")
#         client = boto3.client(
#             'sqs', 
#             aws_access_key_id = ACCESS_KEY, 
#             aws_secret_access_key = SECRET_KEY, 
#             region_name = REGION
#             )

#         response = client.send_message(
#             QueueUrl=queueURL,
#             MessageBody=json.dumps(messageBody)
#         )

#         return response

#     except KeyError as missing:
#         return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

#     except Exception as err:
#         return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

# def recieveSQS():
#     try:
#         queueURL = request.get_json()["QueueUrl"]
#         client = boto3.client(
#             'sqs', 
#             aws_access_key_id = ACCESS_KEY, 
#             aws_secret_access_key = SECRET_KEY, 
#             region_name = REGION
#             )

#         response = client.receive_message(
#             QueueUrl=queueURL,
#             MaxNumberOfMessages=10,
#             WaitTimeSeconds=3
#         )
#         return response

#     except KeyError as missing:
#         return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

#     except Exception as err:
#         return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST
        