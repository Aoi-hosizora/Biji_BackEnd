class ImageTypeError(Exception):
    '''
    图片类型错误
    '''
    def __init__(self, ext: str = ""):
        self.ext = ext

    def __str__(self):
        return "Image type \"%s\" not supported" % self.ext