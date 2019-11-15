from datetime import datetime
import random


def get_ext(filename: str) -> str:
    """ 获得文件后缀名 """
    return filename.split(".")[-1].lower()


def is_image(filename: str) -> bool:
    """ 根据后缀名判断 图片类型 """
    ext = get_ext(filename)
    supported = ['jpg', 'png', 'jpeg', 'bmp']
    return ext in supported


def is_document(filename: str) -> bool:
    """ 通过后缀名判断 文档类型 """
    ext = get_ext(filename)
    supported = ['txt', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'zip', 'rar']
    return ext in supported


def create_uuid() -> str:
    """
    生成唯一文件名: 2019_11_16_04_06_19_65_XX (18位)
    """
    nowTime = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-4]
    randomNum = random.randint(0, 100)
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum
