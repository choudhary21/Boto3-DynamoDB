from src.extensions import db

class ExportToS3(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    TableId = db.Column(db.Integer)
    S3Bucket = db.Column(db.String(50))
    LocationString = db.Column(db.String(100))
    def __init__(self, TableId, S3Bucket, LocationString):
        self.TableId = TableId
        self.S3Bucket = S3Bucket
        self.LocationString = LocationString

class ListExports(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    Bucket=db.Column(db.String(50))
    JsonFile=db.Column(db.String(100))
    def __init__(self, JsonFile, Bucket):
        self.JsonFile=JsonFile
        self.Bucket=Bucket

class ListTables(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    Table=db.Column(db.String(50))
    pitr_status = db.Column(db.Boolean)
    def __init__(self, Table):
        self.Table=Table
        self.pitr_status = None

# class UpdatePITR(db.Model):
#     _id = db.Column(db.Integer, primary_key = True)
#     tableName = db.Column(db.String(50))
#     pitr_status= db.Column(db.String(10))
#     def __init__(self, tableName, pitr_status):
#         self.tableName = tableName
#         self.pitr_status = pitr_status

