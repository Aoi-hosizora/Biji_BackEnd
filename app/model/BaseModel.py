class BaseModel(object):
    """
    抽象模型基类，要求必须重写 to_json() 方法返回字典
    """

    def to_json(self) -> dict:
        """
        Must Override
        """
        # return self.__dict__
        pass
