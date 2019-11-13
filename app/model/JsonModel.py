from typing import List


class JsonModel(object):
    """
    抽象模型基类，要求必须重写 to_json() 方法返回字典
    """

    def to_json(self) -> dict:
        """
        Must Override
        """
        # return self.__dict__
        pass  # <class 'NoneType'>

    @staticmethod
    def to_jsons(objs: List) -> List[dict]:
        """
        统一的返回 Json 列表
        """
        returns = []
        for obj in objs:
            if not isinstance(obj, JsonModel) or not isinstance(obj.to_json(), dict):
                continue
            returns.append(obj.to_json())
        return returns
