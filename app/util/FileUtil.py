import os
from datetime import datetime
import random

# from werkzeug.utils import secure_filename  # 已修改中文支持


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
    supported = ['txt', 'md', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'zip', 'rar']
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


def saveFile(file, path: str, file_image: bool) -> (str, bool, bool):
    """
    保存文件
    :param file: request.files.get('file')
    :param path: f'{Config.UPLOAD_FOLDER}/xxx/{g.user}/' 不加最后的文件名
    :param file_image: 上传的文件是否是图片,判断后缀名
    :return: 文件格式 (is_image / is_document) 正确，是否保存成功 (os.path.exists)
    """
    # filename: str = secure_filename(file.filename)  # 旧文件名
    filename: str = file.filename  # 旧文件名
    if file_image and not is_image(filename):  # 非图片
        return '', False, False
    if not file_image and not (is_image(filename) or is_document(filename)):  # 非文档
        return '', False, False

    filename: str = f'{create_uuid()}.{get_ext(filename)}'  # 新文件名 201911160411418089.jpg
    if not os.path.exists(path):
        os.makedirs(path)
    filepath = os.path.join(path, filename)  # 最终文件路径名 ./usr/img/1111/201911160411418089.jpg
    file.save(filepath)

    if not os.path.exists(filepath):  # 保存失败
        return '', True, False
    else:  # 保存成功，返回路径
        return filename, True, True


def createFile(filename: str) -> bool:
    """
    新建文件
    """
    filepath = filename[0:filename.rfind(os.sep)]
    if not os.path.isdir(filepath):
        os.makedirs(filepath)
    if not os.path.isfile(filename):
        fd = open(filename, 'w')
        fd.close()
    return os.path.exists(filename)
