from app.Utils import TypeUtil

from app.Modules.Note.Exceptions.ImageUploadError import ImageUploadError 
from app.Modules.Note.Exceptions.ImageTypeError import ImageTypeError 
from app.Modules.Note.Exceptions.ImageNotExistError import ImageNotExistError 

from werkzeug import secure_filename
import os

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
            return filename
        else:
            raise ImageUploadError(filename)
    else:
        raise ImageUploadError()
    
def getUserImg(username: str, filename: str):
    '''
    获得用户笔记图片
    '''
    filepath = './usr/img/{}/'.format(username)
    filepath = os.path.join(filepath, filename)

    if not os.path.exists(filepath):
        raise ImageNotExistError(filename)

    with open(filepath, 'rb') as f:
        return f.read()