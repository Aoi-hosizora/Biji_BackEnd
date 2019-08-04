from app.Database.FileDAO import FileDAO
from app.Utils import TypeUtil

from app.Modules.File.Models.File import File
from app.Modules.File.Exceptions.FileNotExistError import FileNotExistError
from app.Modules.File.Exceptions.InsertError import InsertError
from app.Modules.File.Exceptions.DeleteError import DeleteError
from app.Modules.File.Exceptions.FileTypeError import FileTypeError
from app.Modules.File.Exceptions.FileUploadError import FileUploadError

from werkzeug.utils import secure_filename

import os


def getAllFiles(username: str, foldername: str) -> [File]:
    '''
    查询所有文件
    '''
    fileDao = FileDAO()
    return fileDao.queryFiles(username, foldername)


def getOneFile(username: str, foldername: str, filename: str) -> File:
    '''
    查询一个文件
    '''
    fileDao = FileDAO()
    ret = fileDao.queryOneFile(username, foldername, filename)
    if ret == None:
        raise FileNotExistError(filename)
    return ret


def insertFile(file: File) -> bool:
    '''
    插入一个文件
    '''
    fileDao = FileDAO()
    if fileDao.insertFile(file):
        return True
    else:
        raise InsertError(file.filename)

def deleteFile(file: File) -> bool:
    '''
    删除一个文件
    '''
    fileDao = FileDAO()
    if fileDao.deleteFile(file):
        return True
    else:
        raise DeleteError(file.filename)


def saveFile(file, username: str):
    '''
    保存用户文件
    '''
    if file:
        filename = secure_filename(file.filename)  # 旧文件名
        ext = TypeUtil.getExt(filename).lower()  # 后缀名
        if not TypeUtil.isFile(filename):  # 判断文件类型
            raise FileTypeError(ext)
        filename = "{}.{}".format(TypeUtil.create_uuid(), ext)  # 新文件名

        filepath = './usr/file/{}/'.format(username)  # 存放文件夹
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filepath = os.path.join(filepath, filename)  # 最终路径
        file.save(filepath)
        if os.path.exists(filepath):
            return (filename, filepath)
        else:
            raise FileUploadError(filename)
    else:
        raise FileUploadError()


def getFile(username: str, filename: str):
    '''
    获得用户文件
    '''
    filepath = './usr/file/{}/'.format(username)
    filepath = os.path.join(filepath, filename)

    if not os.path.exists(filepath):
        raise FileNotExistError(filename)

    with open(filepath, 'rb') as f:
        return f