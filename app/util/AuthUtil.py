from app.config.Config import Config
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def encrypt_password(password) -> str:
    """
    加密密码
    """
    return custom_app_context.encrypt(password)


def verify_password(password, encrypted_password) -> bool:
    """
    验证密码
    """
    return custom_app_context.verify(password, encrypted_password)


def generate_token(uid: int, expiration: int) -> str:
    """
    生成 token，有效期 expiration & uid
    """
    return Serializer(secret_key=Config.SECRET_KEY, expires_in=expiration).dumps({
        'uid': uid
    }).decode('utf-8')
