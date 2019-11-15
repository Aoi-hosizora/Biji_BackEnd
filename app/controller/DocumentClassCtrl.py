from flask import Blueprint
from flask_httpauth import HTTPTokenAuth


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/document/class`
    """

    @auth.login_required
    @blue.route('/', methods=['GET'])
    def GetAllRoute():
        """
        所有文件分组
        :return:
        """
        pass

    @auth.login_required
    @blue.route('/', methods=['POST'])
    def InsertRoute():
        """
        新建文件分组
        """
        pass

    @auth.login_required
    @blue.route('/', methods=['PUT'])
    def UpdateRoute():
        """
        更新文件分组
        """
        pass

    @auth.login_required
    @blue.route('/', methods=['DELETE'])
    def DeleteRoute():
        """
        删除文件分组
        """
        pass

    # @auth.login_required
    # @blue.route('/share', methods=['DELETE'])
    # def ShareRoute():
    #     """
    #     生成文件共享二维码
    #     """
    #     pass
