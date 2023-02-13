from src.extensions import db

class UpdatePITR(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    tableName = db.Column(db.String(50))
    pitr_status= db.Column(db.String(10))
    def __init__(self, tableName, pitr_status):
        self.tableName = tableName
        self.pitr_status = pitr_status

class ExportToS3(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    TableName = db.Column(db.String(50))
    S3Bucket = db.Column(db.String(50))
    ExportTime = db.Column(db.String(50))
    def __init__(self, TableName, S3Bucket, ExportTime):
        self.TableName = TableName
        self.S3Bucket = S3Bucket
        self.ExportTime = ExportTime

class ListExports(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    Bucket=db.Column(db.String(50))
    JsonFile=db.Column(db.String(100))
    def __init__(self, JsonFile, Bucket):
        self.JsonFile=JsonFile
        self.Bucket=Bucket

class ListTables(db.Model):
    # _id = db.Column(db.Integer, primary_key = True)
    tableName=db.Column(db.String(50), primary_key = True)
    def __init__(self, tableName):
        self.tableName=tableName

