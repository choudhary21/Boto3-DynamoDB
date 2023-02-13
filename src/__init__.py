from flask import Flask
import logging
from src.config import *
from .dynamoDB_module import dynamoDB
from .extensions import db
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://abhishek:Opcito123@localhost/boto3_DynamoDB"
db.init_app(app)

with app.app_context():
    from .dynamoDB_module.models import *
    
    db.create_all()

logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")

if app.debug:
    # Fix werkzeug handler in debug mode
    logging.getLogger('werkzeug').disabled = True


app.register_blueprint(dynamoDB)
    

if __name__=="__main__":
    app.run(debug=True)