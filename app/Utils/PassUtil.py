from app.Config import Config
from app.Modules.Auth.Exceptions.LoginError import LoginError
from app.Modules.Auth.Exceptions.TokenTimeoutError import TokenTimeoutError

from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

def hash_password(password) -> str:
    '''
    加密密码
    '''
    return custom_app_context.encrypt(password)

def verify_password(password, dbpass) -> bool:
    '''
    验证密码
    '''
    return custom_app_context.verify(password, dbpass)

# Ref: https://blog.csdn.net/weixin_38639882/article/details/84588208

def generate_token(username, expiration) -> str:
    '''
    生成token(去除b')，有效期 expiration
    '''
    return Serializer(Config.SecretKey, expires_in = expiration).dumps({'username': username}).__str__()[2:-1]

def certify_token(token) -> str:
    '''
    验证token，并返回用户名
    '''
    try:
        data = Serializer(Config.SecretKey).loads(token)
    except SignatureExpired:
        raise TokenTimeoutError()
    except BadSignature:
        raise LoginError()
    username = data['username']
    # TODO 重新登录实现 token 失效
    if username == "":
        raise LoginError()
    return username
