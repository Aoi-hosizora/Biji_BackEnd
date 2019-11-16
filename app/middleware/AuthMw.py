from flask import g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import Serializer, SignatureExpired, BadSignature

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.dao.UserDao import UserDao
from app.database.dao.UserTokenDao import UserTokenDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode


def setup_auth() -> HTTPTokenAuth:
    """
    用户 id 存在 g.user
    """
    auth = HTTPTokenAuth(scheme='Bearer')

    @auth.verify_token
    def verify_token(token: str) -> bool:
        """
        验证 token 内的 ex 与 uid
        """
        if not token:
            return False
        try:
            data = Serializer(Config.SECRET_KEY).loads(token)
            uid: int = data['uid']
        except SignatureExpired as ex:  # 过期
            raise ex
        except BadSignature as ex:  # 错误
            raise ex

        if not isinstance(uid, int) or uid <= 0:  # 格式错误
            return False
        if UserDao().queryUserById(uid) == DbStatusType.NOT_FOUND:  # 无用户
            return False
        if not UserTokenDao().checkToken(token):  # 无登陆
            return False

        g.user = uid
        return True

    @auth.error_handler
    def error_handler():
        return Result.error(ResultCode.UNAUTHORIZED).json_ret()

    return auth
