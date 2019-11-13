class QueryError(Exception):
    """
    请求参数缺失或错误
    """

    def __init__(self, args=None):
        if args is None:
            args = []
        self.args = args

    def __str__(self):
        if not len(self.args) == 0:
            return "Request query params error, arg %s not found or error" % list(self.args)
        else:
            return "Request query params error."
