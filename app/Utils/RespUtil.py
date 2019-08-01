from flask import Response
import json

def jsonRet(dict, code, headers={}):
    '''
    处理响应内容 状态码及除了跨域以外的响应头
    '''
    resp = Response(
        json.dumps(obj=dict, indent=4, ensure_ascii=False).encode("utf-8"), 
        mimetype='application/json'
    )

    for k, v in headers.items():
        resp.headers[k] = v
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status_code = code
    return resp