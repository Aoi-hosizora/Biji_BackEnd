class ImageUploadError(Exception):
    '''
    图片上传错误
    '''
    def __init__(self, filename: str = ""):
        self.filename = filename

    def __str__(self):
        if self.filename == "":
            return "Image upload error"
        else:
            return "Image upload error, filename: \"%s\"" % self.filename