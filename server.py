from app.route.RouteBlue import setup_route_blue
from app.route.ErrorForward import setup_error_forward

from app.middleware.CorsMw import setup_cors
from app.config.Config import Config

from flask import Flask, app

FlaskApp = Flask(__name__)


def setup(flask_app: app.Flask):
    """
    配置中间件 全局设置 蓝图 错误转发
    """
    # middleware
    setup_cors(app=flask_app)

    # config
    flask_app.config['JSON_AS_ASCII'] = False
    flask_app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    flask_app.config['SECRET_KEY'] = Config.SECRET_KEY

    # Module Blues
    setup_route_blue(app=flask_app)

    # Error Forward
    setup_error_forward(app=flask_app)


# nginx + uwsgi + flask + blueprint
setup(FlaskApp)
if __name__ == "__main__":
    FlaskApp.run(
        host=Config.SERVER_HOST, port=Config.SERVER_PORT,
        threaded=True, debug=True
    )
