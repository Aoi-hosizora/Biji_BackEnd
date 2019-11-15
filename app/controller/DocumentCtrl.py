from flask import Blueprint
from flask_httpauth import HTTPTokenAuth


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/document`
    """

    @auth.login_required
    @blue.route('/', methods=['GET'])
    def GetAllRoute():
        """ 所有文件 """
        pass

    @auth.login_required
    @blue.route('/<string:docClass>', methods=['GET'])
    def GetClassRoute(docClass: str):
        """ 分组文件 """
        pass

    @auth.login_required
    @blue.route('/<int:did>', methods=['GET'])
    def GetOneRoute(did: int):
        """ 单个文件 """
        pass

    @auth.login_required
    @blue.route('/', methods=['POST'])
    def InsertRoute():
        """ 插入文件 """
        # TODO 文件操作
        pass

    @auth.login_required
    @blue.route('/', methods=['PUT'])
    def UpdateRoute():
        """ 更新文件 """
        # TODO 文件操作
        pass

    @auth.login_required
    @blue.route('/', methods=['DELETE'])
    def DeleteRoute():
        """ 删除文件 """
        # TODO 文件操作
        pass


"""

@blue_File.route("/get_share", methods=['GET'])
def GetSharedFiles():
    '''
    获取共享的文件
    :return:
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    usernameShared = request.args.get('username')
    foldernameShared = request.args.get('foldername')

    shareCodeJson = FileClassCtrl.shareCode2Json(usernameShared, foldernameShared)

    if FileCtrl.checkShareCode(usernameShared + foldernameShared, shareCodeJson):
        
        fileClass = FileClassCtrl.getOneFileClass(usernameShared, DocumentClass(0, foldernameShared))
        files = FileCtrl.getAllFiles(usernameShared, foldernameShared)
        for file in files:
            file.username = username
        if FileClassCtrl.getOneFileClass(username, fileClass) is None:
            FileClassCtrl.insertFileClass(username, fileClass)
        FileCtrl.pushFile(username, files)

        return RespUtil.jsonRet(
            data=Message(
            message="Get share files success",
        ).toJson(),
            code=ErrorUtil.Success,
            headers={'Authorization': newToken} if newToken != "" else {}
        )
    return RespUtil.jsonRet(
        data=Message(
            message="Get share files fail",
        ).toJson(),
        code=ErrorUtil.NotFound,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


"""
