
# # Input validation for Table name in DynamoDB
def validate_table(table):
    if not isinstance(table, str):
        raise Exception("table name must be string")
    elif len(table) < 3:
        raise Exception("length of table name cannot be less than 3")

# # Input validation for S3 Bucket name 
def validate_bucket(bucket):
    if not isinstance(bucket, str):
        raise Exception("bucket name must be string")
    elif len(bucket) < 3:
        raise Exception("bucket must have length greater than or equal to 3")

# # Input validation for Maximum results
# def validate_maxRes(maxRes):
#     if not isinstance(maxRes, int):
#         raise Exception("Maximum results must be integer")