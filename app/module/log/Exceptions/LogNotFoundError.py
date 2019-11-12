class LogNotFoundError(Exception):
    '''
    日志类型未知
    '''
    def __init__(self, log: str = ""):
        self.log = log

    def __str__(self):
        if self.log == None or self.log == "":
            return "Log module not found"
        else:
            return "Log module: \"%s\" not found" % self.log