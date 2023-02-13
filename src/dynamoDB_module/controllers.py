from flask import request, jsonify
from src.config import *
from http import HTTPStatus
import boto3
from .constants import *
from flask import current_app
from .service import validate_table
from .service import validate_bucket
from .service import validate_PITR
from .models import *
from src.extensions import db
from src.utils import create_client, create_resource
import json
# from .service import validate_maxRes

# API for enabling the PITR for a table of DynamoDB
def update_PITR():
    try:
        table = request.get_json()['table']
        pitr_status = request.get_json()['pitr']
        current_app.logger.info("Creating client instance for updating PITR")
        validate_PITR(pitr_status)
        client = create_client('dynamodb')           
        # Checking if PITR is already enabled
        pitr_response = client.describe_continuous_backups(
            TableName= table
            )
        pitr = pitr_response["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]["PointInTimeRecoveryStatus"]
        if pitr == "ENABLED" and pitr_status == True:
            return jsonify({"message" : PITR_ALREADY_ENABALED}), HTTPStatus.OK
        if pitr == "DISABLED" and pitr_status == False:
            return jsonify({"message" : PITR_ALREADY_DISABLED}), HTTPStatus.OK

        # print("pitr: ", pitr_response["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]["PointInTimeRecoveryStatus"])
        current_app.logger.info("Sending request to enable PITR")

        response = client.update_continuous_backups(
            TableName = table,
            PointInTimeRecoverySpecification={
                'PointInTimeRecoveryEnabled': pitr_status   
            }
        )
        print("res",response)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            # updating the DB
            tableExist = UpdatePITR.query.filter(UpdatePITR.tableName == table).first()
            if tableExist:
                tableExist.pitr_status = response['ContinuousBackupsDescription']['PointInTimeRecoveryDescription']['PointInTimeRecoveryStatus']
                db.session.commit()
            else:
                update_pitr = UpdatePITR(table,
                response['ContinuousBackupsDescription']['PointInTimeRecoveryStatus']
                )
                db.session.add(update_pitr)
                db.session.commit()
                current_app.logger.info("Sending successful response after enabling the PITR")
                if pitr_status == True:
                    return jsonify({"message" : PITR_ENABALED}), HTTPStatus.OK
                else:
                    return jsonify({"message" : PITR_DISABLED}), HTTPStatus.OK
        else:
            raise Exception(SOMETHING_WENT_WRONG)
        
    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        if str(err).__contains__("Table not found"):
            err = "Table not found" 
        elif str(err).__contains__("PITR value should be Boolean"):
            err = "PITR value should be Boolean"
        
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

# API for Export to S3 (json file)

def exportToS3():
    status = True
    try:
        # arn = request.get_json()["TableArn"]
        tableName = request.get_json()["TableName"]
    # Input validation for S3 Table name  
        validate_table(tableName)
        bucket = request.get_json()["S3Bucket"]
    # Input validation for S3 Bucket name 
        validate_bucket(bucket)
        # s3 = boto3.client('s3')
        s3 = create_client('s3')
        # bucket = s3.Bucket(bucket)
        # bucket_list = s3.list_buckets()['Buckets']
        buckets = list(map(lambda bucket: bucket['Name'], s3.list_buckets()['Buckets']))
        
        if bucket not in buckets:
            raise Exception(f"Bucket {bucket} does not exist.")
        
        current_app.logger.info("Creating client instance for exporting to s3")
        client = create_client('dynamodb')
        table = client.describe_table(TableName=tableName)
        table_arn = table['Table']['TableArn']        

        response = client.export_table_to_point_in_time(
            TableArn = table_arn,
            S3Bucket = bucket,
            ExportFormat="DYNAMODB_JSON"
        )
        exporttoS3 = ExportToS3(tableName, bucket, response["ExportDescription"]["ExportTime"])
        db.session.add(exporttoS3)
        db.session.commit()
        
        print("res",response)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return jsonify({"message" : EXPORTED_TO_S3}), HTTPStatus.OK
        
    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        if str(err).__contains__(f"Table: {tableName} not found"):
            err = f"Table {tableName} not found"
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

# API for List all the exported json files

def listExports():
    data = []
    try:
        bucket = request.get_json()["bucket"]
        current_app.logger.info("Creating client instance for listing all exported files")
        client = create_resource('s3')
        response = client.Bucket(bucket)
        summaries = response.objects.all()
        # print("files", summaries)
        if summaries == None: # condition if we get none response
            raise Exception(NONE_VALUE)
        for files in summaries:
            # print("data: ", files)
            if(files.key[-5:] == ".json"):
                data.append(files.key)
                jsonFile = ListExports.query.filter_by(JsonFile=files.key).all()
                if not jsonFile:
                    exportedFiles = ListExports(files.key, bucket)
                    db.session.add(exportedFiles)
                    db.session.commit()

        current_app.logger.info(str(data))
        return jsonify(data), HTTPStatus.OK

    except KeyError as key:
        return {"error" : f"Parameter {key} is mising"}, HTTPStatus.BAD_REQUEST
        
    except Exception as err:
        if str(err).__contains__("bucket does not exist"):
            err = "bucket does not exist" 
        elif str(err).__contains__("Access Denied"):
            err = "access denied for this bucket"
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST

def listTables():
    try:
        current_app.logger.info("Creating client instance for listing all tables")
        client = create_client('dynamodb')

        response = client.list_tables()  
        # ExclusiveStartTableName = tableName, Limit = limit
        # queueName = request.get_json()["QueueName"]

        # sqsClient = create_client('sqs')    
        # queueName = sqsClient.get_queue_url(QueueName=queueName)
        # queueURL = queueName['QueueUrl']

        # for table in response["TableNames"]:
        #     Tables = ListTables.query.filter_by(tableName=table).all()
        #     sqsResponse = sqsClient.send_message(
        #         QueueUrl = queueURL,
        #         MessageBody = table
        #     )
        #     if not Tables:
        #         listTables = ListTables(table)
        #         db.session.add(listTables)
        #         db.session.commit()
        return jsonify(response["TableNames"]), HTTPStatus.OK

    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as err:
        return jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST