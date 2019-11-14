from app.route.RouteBlue import register_modules_blue
from app.route.ErrorForward import setup_error_forward

from app.middleware.CorsMw import setup_cors
from app.config import Config

from flask import Flask, app

FlaskApp = Flask(__name__)
host = '0.0.0.0'
port = 8001


def setup(flask_app: app.Flask):
    """
    配置中间件 全局设置 蓝图 错误转发
    """
    # middleware
    setup_cors(app=flask_app)

    # config
    flask_app.config['JSON_AS_ASCII'] = False
    flask_app.config['UPLOAD_FOLDER'] = "./usr/"
    flask_app.config['SECRET_KEY'] = "$$AOI@@HOSI^^ZORA##"
    Config.SecretKey = flask_app.config['SECRET_KEY']

    # Module Blues
    register_modules_blue(app=flask_app)

    # Error Forward
    setup_error_forward(app=flask_app)


# nginx + uwsgi + flask + blueprint
setup(FlaskApp)
if __name__ == "__main__":
    FlaskApp.run(host=host, port=port, threaded=True, debug=True)
