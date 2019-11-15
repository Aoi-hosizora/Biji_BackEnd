from flask import Blueprint
from flask_httpauth import HTTPTokenAuth


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/document`
    """

    @auth.login_required
    @blue.route('/', methods=['GET'])
    def GetAllRoute():
        pass
