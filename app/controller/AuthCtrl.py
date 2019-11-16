from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.dao.UserDao import UserDao
from app.database.dao.UserTokenDao import UserTokenDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.route.ParamType import ParamError, ParamType
from app.util import AuthUtil


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/auth`
    """

    @blue.route("/login", methods=['POST'])
    def LoginRoute():
        """ 登录 """
        try:
            username = request.form['username']  # 必须
            password = request.form['password']  # 必须
            ex = request.form.get('expiration')  # 可选
            if not ex or ex == 0:
                ex = Config.LOGIN_TOKEN_EX
        except:
            raise ParamError(ParamType.FORM)

        status, user = UserDao().checkUserPassword(username, password)
        if status == DbStatusType.FAILED:
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("Password Error").json_ret()
        elif status == DbStatusType.NOT_FOUND:
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("User Not Found").json_ret()
        else:  # Success
            token = AuthUtil.generate_token(user.id, ex)
            if not UserTokenDao().addToken(user.id, token):  # Add to redis
                return Result.error(ResultCode.UNAUTHORIZED).setMessage("Login Failed").json_ret()

            return Result.ok().setData(user.to_json()).json_ret(headers={'Authorization': 'Bearer ' + token})

    @blue.route("/register", methods=['POST'])
    def RegisterRoute():
        """ 注册 """
        try:
            username = request.form['username']  # 必须
            password = request.form['password']  # 必须
        except:
            raise ParamError(ParamType.FORM)

        # Format
        if not (Config.FMT_USERNAME_MIN <= len(username) <= Config.FMT_USERNAME_MAX and Config.FMT_PASSWORD_MIN <= len(password) <= Config.FMT_PASSWORD_MAX):
            return Result.error(ResultCode.BAD_REQUEST).setMessage('Format Error').json_ret()

        # Database
        status, new_user = UserDao().insertUser(username, password)
        if status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Register Failed").json_ret()
        elif status == DbStatusType.FOUNDED:
            return Result.error(ResultCode.HAS_EXISTED).setMessage("User Existed").json_ret()
        else:  # Success
            return Result.ok().setData(new_user.to_json()).json_ret()

    @blue.route("/logout", methods=['POST'])
    @auth.login_required
    def LogoutRoute():
        """ 注销 """
        count = UserTokenDao().removeToken(g.user)
        if count == 0:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Logout Failed").json_ret()
        else:
            return Result.ok().putData("count", count).json_ret()
