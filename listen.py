from app.Routes.BluesHandler import register_modules_blue
from app.Routes.ErrorHandler import register_error_forward

from app.Middleware.CorsMw import setupCors
from app.Config import Config

from flask import Flask, app

FlaskApp = Flask(__name__)
host = '0.0.0.0'
port = 8001

def setup(app: app.Flask):
    '''
    配置中间件 全局设置 蓝图 错误转发
    '''
    # Middleware
    setupCors(app=app)

    # Config
    app.config['JSON_AS_ASCII'] = False
    app.config['UPLOAD_FOLDER'] = "./usr/"
    app.config['SECRET_KEY'] = "$$AOI@@HOSI^^ZORA##"
    Config.SecretKey = app.config['SECRET_KEY']
    
    # Module Blues
    register_modules_blue(app=app)

    # Error Forward
    register_error_forward(app=app)

# nginx + uwsgi + flask + blueprint
setup(FlaskApp)
if __name__ == "__main__":
    FlaskApp.run(host=host, port=port)
