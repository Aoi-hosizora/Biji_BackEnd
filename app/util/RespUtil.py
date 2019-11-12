from flask import Response, make_response
import json
import time

from app.database.TokenDAO import TokenDAO
from app.module.auth.Exceptions.LoginError import LoginError
from app.util.exception.AuthNoneError import AuthNoneError
from app.util import PassUtil


def jsonRet(data: dict or bytes, code: int, headers: dict = None, isImage: bool = False) -> Response:
    """
    处理 响应内容 状态码 响应头 (跨域) 二进制文件
    """
    if headers is None:
        headers = {}

    if not isImage:
        # data: dict
        resp = Response(
            json.dumps(obj=data, indent=4, ensure_ascii=False).encode("utf-8"),
            mimetype='application/json'
        )
    else:
        # data: Image Bytes
        resp = make_response(data)

    resp.status_code = code
    for k, v in headers.items():
        resp.headers[k] = v
    # CORS
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


def getAuthUser(headers: dict) -> [str, str]:
    """
    获取并判断 token 可用性并且返回用户名或抛错

    @return `username` `newToken`
    """
    token = headers.get("Authorization")

    # 无 Token 头
    if token is None:
        raise AuthNoneError()
    tokenDao = TokenDAO()

    isExist, isClear = tokenDao.checkToken(token)

    if isExist:
        # redis 存在 token, 直接查詢
        return PassUtil.certify_token(token), ""
    elif isClear:
        # redis 不存在 token, 并且即將被刪除, 插入新 token 并返回
        usr = PassUtil.certify_token(token)
        ex, ct = PassUtil.get_ex_ct_from_token(token)
        newEx = int(ex - (time.time() - ct))
        newToken = PassUtil.generate_token(username=usr, expiration=newEx)
        tokenDao.addToken(token=newToken, username=usr)
        return usr, newToken
    else:
        # redis 不存在 token, 并且也已經被刪除
        # TODO 再使用老 token 報錯
        raise LoginError()
