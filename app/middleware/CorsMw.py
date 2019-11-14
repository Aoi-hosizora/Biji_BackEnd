from flask.app import Flask
from flask_cors import CORS


def setup_cors(app: Flask) -> CORS:
    """
    跨域中间件
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    return cors
