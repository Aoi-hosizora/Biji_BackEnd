from app.Utils import TypeUtil
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError

from app.Modules.Note.Exceptions.ImageUploadError import ImageUploadError 
from app.Modules.Note.Exceptions.ImageTypeError import ImageTypeError 
from app.Modules.Note.Exceptions.ImageNotExistError import ImageNotExistError
from app.Modules.Note.Models.DelImg import DelImg

from werkzeug.utils import secure_filename
import os, json

def getImgsFromReqData(reqdata: str) -> [DelImg]:
    '''
    从 Req 的 headers 中获取 DelImg[]

    `getImgsFromReqData(request.get_data(as_text=True))`
    '''
    try:
        postjsons = json.loads(reqdata)
        ret = []
        for postjson in postjsons:
            ret.append(checkJson(json.loads(postjson)))
    
    except:
        # 解析错误
        raise BodyRawJsonError()
    
    return ret

def checkJson(postjson) -> DelImg:
    '''
    检查 Json 并转化
    '''
    keys = ['username', 'filename']
    nonePostKeys = [
        key for key in keys
        if key not in postjson or postjson[key] == None
    ]
    if not len(nonePostKeys) == 0:
        # 缺少参数
        raise(BodyRawJsonError(nonePostKeys))

    if not len(postjson) == len(keys):
        # 参数过多
        raise BodyRawJsonError()

    try:
        return DelImg(*[postjson[key] for key in keys])
    except:
        # 内容错误
        raise BodyRawJsonError()

def saveUserImg(username: str, img) -> str:
    '''
    保存用户笔记图片
    '''
    if img:
        filename = secure_filename(img.filename) # 旧文件名
        ext = TypeUtil.getExt(filename).lower() # 后缀名
        if not TypeUtil.isImg(filename): # 判断文件类型
            raise ImageTypeError(ext)
        filename = "{}.{}".format(TypeUtil.create_uuid(), ext) # 新文件名

        filepath = './usr/img/{}/'.format(username) # 存放文件夹
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            
        filepath = os.path.join(filepath, filename) # 最终路径
        img.save(filepath)
        if os.path.exists(filepath):
            return filepath
        else:
            raise ImageUploadError(filepath)
    else:
        raise ImageUploadError()
    
def getUserImg(username: str, filename: str):
    '''
    获得用户笔记图片
    '''
    filepath = './usr/img/{}'.format(username)
    filepath = os.path.join(filepath, filename)

    if not os.path.exists(filepath):
        raise ImageNotExistError(filename)

    with open(filepath, 'rb') as f:
        return f.read()

def delUsrImgs(username: str, delImgs: [DelImg]) -> int:
    '''
    检查并删除用户图片，返回个数
    '''
    l = 0
    for delImg in delImgs:
        usr, name = delImg.username, delImg.imgName
        if usr != username:
            continue
        filepath = './usr/img/{}/{}'.format(username, name)
        if os.path.exists(filepath):
            os.remove(filepath)
            if not os.path.exists(filepath):
                l = l + 1
    return l