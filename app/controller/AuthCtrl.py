from flask import Blueprint, request

from app.database.DbErrorType import DbErrorType
from app.database.dao.UserDao import UserDao
from app.model.vo.Result import Result
from app.model.vo.ResultCode import ResultCode
from app.route.ParamError import ParamError, ParamType
from app.util import AuthUtil


def apply_blue(blue: Blueprint):
    """
    应用 Blueprint Endpoint 路由映射
    """

    @blue.route("/login", methods=['POST'])
    def LoginRoute():
        """
        登录
        """
        try:
            username = request.form['username']
            password = request.form['password']
            ex = request.form['expiration']
        except:
            raise ParamError(ParamType.FORM)

        ret = UserDao().checkUserPassword(username, password)
        if ret == DbErrorType.FAILED:
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("Password Error").json_ret()
        elif ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("User Not Found").json_ret()
        else:  # Success
            token = AuthUtil.generate_token(username, ex)
            # TODO Redis
            return Result.ok().json_ret(headers={'Authorization': token})

    @blue.route("/register", methods=['POST'])
    def RegisterRoute():
        """
        注册
        """
        try:
            username = request.form['username']
            password = request.form['password']
        except:
            raise ParamError(ParamType.FORM)

        ret = UserDao().insertUser(username, password)
        if ret == DbErrorType.FAILED:
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("Register Failed").json_ret()
        elif ret == DbErrorType.FOUNDED:
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("User Existed").json_ret()
        else:  # Success
            return Result.ok().putData("username", username).json_ret()

    @blue.route("/logout", methods=['POST'])
    def LogoutRoute():
        """
        注销
        """
        # TODO Redis
        # tokenDao = TokenDao()
        # return tokenDao.removeToken(username)
        pass
