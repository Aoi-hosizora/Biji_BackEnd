import json
from typing import List, Tuple
from datetime import datetime

from app.database.RedisHelper import RedisHelper


class ShareCodeDao(RedisHelper):
    sc_prefix = 'biji_sc_'

    def __init__(self):
        super(ShareCodeDao, self).__init__()

    def addShareCode(self, uid: int, dids: List[int], ex: int) -> str:
        """
        :param: uid 用户 id
        :param: dids 文档 id 列表
        :return: 分享码 '' for error
        """
        now = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-4]  # 2019111919004491
        uuid = '{}_{}'.format(uid, now)
        sc = self.sc_prefix + uuid  # biji_sc_23_2019111919004491
        ok = self.db.set(name=sc, value=json.dumps(dids), ex=ex)
        return sc if ok else ''

    def getShareContent(self, sc: str) -> Tuple[int, List[int]]:
        """
        读取 分享码对应的文档编号集
        :return: (uid, [])
        """
        content = self.db.get(name=sc)  # biji_sc_23_2019111919004491
        ids: [str] = json.loads(content)
        uid: int = ids[len(self.sc_prefix):-len('2019111919004491')-1]
        return uid, ids

    def getUserShareCodes(self, uid: int) -> List[int]:
        """
        获取用户所有的共享码
        """
        pattern = f'{self.sc_prefix}_{uid}_*'
        values = self.db.keys(pattern=pattern)
        return values

    def removeShareCodes(self, uid: int, scs: List[str]) -> int:
        """
        删除 共享码 (多)
        :return: 删除个数
        """
        scs = list(filter(lambda code: code.startswith(self.sc_prefix + str(uid)), scs))  # biji_sc_23
        return self.db.delete(*scs)

    def removeUserShareCodes(self, uid: int) -> int:
        """
        删除用户所有的共享码
        :return: 删除个数
        """
        count = self.db.delete(*self.getUserShareCodes(uid))
        return count
