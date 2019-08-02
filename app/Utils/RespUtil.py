from flask import Response, make_response
import json

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

def getAuthUser(headers) -> str:
    '''
    获取并判断 token 可用性并且返回用户名或抛错
    '''
    token = headers.get("Authorization")

    if token == None:
        raise AuthNoneError()
    tokenDao = TokenDAO()
    if tokenDao.checkToken(token):
        return PassUtil.certify_token(token)
    else:
        raise LoginError()
