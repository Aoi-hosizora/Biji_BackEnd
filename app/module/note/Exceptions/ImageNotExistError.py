class ImageNotExistError(Exception):
    '''
    图片不存在
    '''
    def __init__(self, filename: str = ""):
        self.filename = filename

    def __str__(self):
        return "Image \"%s\" not exist" % self.filename