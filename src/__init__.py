from flask import Flask
import logging
from .dynamoDB_module import dynamoDB
from .extensions import db
from .dynamoDB_module.models import *

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://kedar:Kedar123@localhost/DynamoDB"
db.init_app(app)

with app.app_context():
    db.create_all()

logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")

if app.debug:
    # Fix werkzeug handler in debug mode
    logging.getLogger('werkzeug').disabled = True

app.register_blueprint(dynamoDB)

@app.route("/",methods=["GET"])
def index():
    return "Hello World"
    
if __name__=="__main__":
    app.run(debug=True)