class FileUploadError(Exception):
    '''
    文件上传错误
    '''
    def __init__(self, filename: str = ""):
        self.filename = filename

    def __str__(self):
        if self.filename == "":
            return "File upload error"
        else:
            return "File upload error, filename: \"%s\"" % self.filename