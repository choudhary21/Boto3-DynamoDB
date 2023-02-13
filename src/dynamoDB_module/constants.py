PITR_ENABALED = "Point-In-Time-Recovery enabled successfully"
PITR_DISABLED = "Point-In-Time-Recovery disabled successfully"
PITR_ALREADY_ENABALED = "Point-in-time-recovery is already enabled"
PITR_ALREADY_DISABLED = "Point-in-time-recovery is already disabled"
FAILED_VALIDATION = "Parameter validation failed"
TABLE_EXPORTED = "Table successfully exported to s3"
MESSAGE_PUSHED = "Message pushed successfully in SQS queue"
NONE_VALUE = "Something went wrong! Please check the credential you entered"
SOMETHING_WENT_WRONG = "something went wrong! Please try again."
EXPORTED_TO_S3 = "Successfully exported the file to S3 bucket"
TableNotFoundException = "when calling the DescribeContinuousBackups operation: Table not found:"

# possibilities 

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
        
# if "PointInTimeRecoverySpecification"== True:
# return jsonify({"message" : PITR_ENABALED}), HTTPStatus.OK
# elif "PointInTimeRecoverySpecification"== False:
# return jsonify({"message" : PITR_DISABLED}), HTTPStatus.OK

# {'ExportDescription':
#          {'ExportArn': 'arn:aws:dynamodb:us-east-1:300023816116:table/Movie/export/01675919594970-b56eedd7', 
#         'ExportStatus': 'IN_PROGRESS', 
#         'StartTime': datetime.datetime(2023, 2, 9, 10, 43, 14, 970000, tzinfo=tzlocal()), 
#         'TableArn': 'arn:aws:dynamodb:us-east-1:300023816116:table/Movie', 
#         'TableId': '9a958dc7-9d06-49bf-99b8-feb8131a1e05', 
#         'ExportTime': datetime.datetime(2023, 2, 9, 10, 43, 14, 970000, tzinfo=tzlocal()), 
#         'ClientToken': '90628cbd-b22e-4fcd-9ba3-fdca04be526a', 'S3Bucket': 'my-demo1', 
#         'S3SseAlgorithm': 'AES256', 
#         'ExportFormat': 'DYNAMODB_JSON'}, 
 
# 'ResponseMetadata': {'RequestId': 'N2C1H40SA2L59MML1H1F7KI9SRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 
#                 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 09 Feb 2023 05:13:15 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '452', 'connection': 'keep-alive', 'x-amzn-requestid': 'N2C1H40SA2L59MML1H1F7KI9SRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2802263589'},
#                 'RetryAttempts': 0}}