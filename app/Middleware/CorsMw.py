from flask.app import Flask
from flask_cors import CORS

def setupCors(app: Flask):
    cors = CORS(app, resources={r"/*": {"origins": "*"}})