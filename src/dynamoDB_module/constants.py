FAILED_VALIDATION = "Parameter validation failed"
PITR_ENABALED = "Point-In-Time-Recovery enabled successfully"
NONE_VALUE = "Something went wrong! Please check the credential you entered"
PITR_ALREADY_ENABALED = "Point-in-time-recovery is already enabled"

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