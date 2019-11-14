from flask import g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import Serializer, SignatureExpired, BadSignature

from app.config import Config
from app.model.vo.Result import Result
from app.model.vo.ResultCode import ResultCode


def setup_auth() -> HTTPTokenAuth:
    auth = HTTPTokenAuth(scheme='Bearer')

    @auth.verify_token
    def verify_token(token: str) -> bool:
        if not token:
            return False
        try:
            data = Serializer(Config.SecretKey).loads(token)
            username: str = data['username']
            if username.strip(' \t'):
                g.username = username
                return True
        except SignatureExpired as ex:
            raise ex
        except BadSignature as ex:
            raise ex
        return False

    @auth.error_handler
    def error_handler():
        return Result.error(ResultCode.UNAUTHORIZED)

    return auth
