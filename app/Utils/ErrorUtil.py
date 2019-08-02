from app.Models.Message import Message

Success = 200
NotFound = 404
InternalServerError = 500
MethodNotAllowed = 405
Forbidden = 403
BadRequest = 400

# RegisterError
NotAcceptable = 406
# LoginError
UnAuthorized = 401

def getErrorDetail(error: TypeError) -> str:
    '''
    获取错误提示详情
    '''
    return error.__str__()

def getErrorMessageJson(error: TypeError, title: str) -> dict:
    '''
    获取错误 Message Json
    '''
    return Message(message=title, detail=getErrorDetail(error)).toJson()