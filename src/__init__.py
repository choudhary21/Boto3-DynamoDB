from flask import Flask
import logging



app = Flask(__name__)
# logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO,
#                     format="%(asctime)s %(levelname)s %(name)s: %(message)s")

# if app.debug:
#     # Fix werkzeug handler in debug mode
#         logging.getLogger('werkzeug').disabled = True

@app.route("/",methods=["GET"])
def index():
    return "Hello World"
    

if __name__=="__main__":
    app.run(debug=True)