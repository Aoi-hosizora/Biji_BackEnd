class ScheduleUploadError(Exception):
    '''
    课表上传错误
    '''
    def __init__(self, username: str):
        self.user = username

    def __str__(self):
        return "Schedule of user \"%s\" upload error" % self.user
