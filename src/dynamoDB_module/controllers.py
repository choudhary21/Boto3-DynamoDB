from flask import request, jsonify
from src.config import *
from http import HTTPStatus
import boto3
from .constants import *
from flask import current_app
from .service import validate_table
from .service import validate_bucket
from src.utils import create_client
from .models import *
from src.extensions import db

# from .service import validate_maxRes

# API for enabling the PITR for a table of DynamoDB
def update_PITR():
    try:
        table = request.get_json()['table']
        current_app.logger.info("Creating client instance for updating PITR")
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

# API for Export to S3 (json file)

def exportToS3():
    status = False
    try:
        arn = request.get_json()["TableArn"]
        tableName = request.get_json()["TableName"]
    # Input validation for S3 Table name  
        validate_table(tableName)
        bucket = request.get_json()["S3Bucket"]
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
            TableName=tableName
            )
        table_arn = table['Table']['TableArn']        

        response = client.export_table_to_point_in_time(
            TableArn = table_arn,
            S3Bucket = bucket,
            ExportFormat="DYNAMODB_JSON"
        )
        exporttoS3 = ExportToS3(tableName, bucket, response["ExportDescription"]["ExportTime"])
        db.session.add(exporttoS3)
        db.session.commit()
        return response

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

# API for List all the exported json files

def listExports():
    data = []
    try:
        bucket = request.get_json()["Bucket"]
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
        # summaries = summaries.split("/ ")
        print("files", summaries)
        if summaries == None: # condition if we get none response
            raise Exception(NONE_VALUE)
        for files in summaries:
            # print("data: ", files)
            if(files.key[-5:] == ".json"):
                data.append(files.key[12:])

        listExports = ListExports(bucket, data)
        db.session.add(listExports)
        db.session.commit()

        return jsonify(data), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST
        
    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

def listTables():
    try:
        current_app.logger.info("Creating client instance for listing all tables")
        client = boto3.client(
            'dynamodb',
            aws_access_key_id = ACCESS_KEY, 
            aws_secret_access_key = SECRET_KEY, 
            region_name = REGION
            )

        response = client.list_tables()  
        # ExclusiveStartTableName = tableName, Limit = limit
        queueName = request.get_json()["QueueName"]

        sqsClient = boto3.client(
            'sqs',
            aws_access_key_id = ACCESS_KEY,
            aws_secret_access_key = SECRET_KEY,
            region_name = REGION
        )    
        queueName = sqsClient.get_queue_url(
            QueueName=queueName)
        queueURL = queueName['QueueUrl']

        
        for table in response["TableNames"]:
            Tables = ListTables.query.filter_by(tableName=table).all()
            sqsResponse = sqsClient.send_message(
                QueueUrl = queueURL,
                MessageBody = table
            )
            
            if not Tables:
                listTables = ListTables(table)
                db.session.add(listTables)
                db.session.commit()

        return jsonify(response["TableNames"]), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST