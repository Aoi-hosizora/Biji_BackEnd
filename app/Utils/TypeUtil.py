import datetime
import random

def getExt(filename: str) -> str:
    '''
    获得文件后缀名
    '''
    return filename.split(".")[-1].lower()

def isImg(filename: str) -> bool:
    '''
    通过文件后缀名判断图片类型
    '''
    ext = getExt(filename)
    supported = ['jpg', 'png', 'jpeg', 'bmp']
    return ext in supported

def create_uuid() -> str:
    '''
    生成唯一文件名
    '''
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    randomNum = random.randint(0, 100)
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum