class LogNotFoundError(Exception):
    '''
    日志类型未知
    '''
    def __init__(self, log: str = ""):
        self.log = log

    def __str__(self):
        if self.log == None or self.log == "":
            return "Log not found"
        else:
            return "Log: \"%s\" not found" % self.log