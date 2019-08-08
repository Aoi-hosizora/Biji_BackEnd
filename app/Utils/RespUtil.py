from flask import Response, make_response
import json
import time

from app.Database.TokenDAO import TokenDAO
from app.Modules.Auth.Exceptions.LoginError import LoginError
from app.Utils.Exceptions.AuthNoneError import AuthNoneError
from app.Utils import PassUtil

def jsonRet(dict, code, headers={}, isImg=False):
    '''
    处理响应内容 状态码及除了跨域以外的响应头
    '''
    if not isImg:
        resp = Response(
            json.dumps(obj=dict, indent=4, ensure_ascii=False).encode("utf-8"), 
            mimetype='application/json'
        )
    else:
        resp = make_response(dict)

    for k, v in headers.items():
        resp.headers[k] = v
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status_code = code
    return resp

def getAuthUser(headers) -> [str, str]:
    '''
    获取并判断 token 可用性并且返回用户名或抛错

    @return `username` `newToken`
    '''
    token = headers.get("Authorization")

    # 无 Token 头
    if token == None:
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
