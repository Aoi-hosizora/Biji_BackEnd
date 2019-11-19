import json
import re
from typing import List, Tuple
from datetime import datetime

from app.database.RedisHelper import RedisHelper
from app.database.dao.DocumentDao import DocumentDao


class ShareCodeDao(RedisHelper):
    sc_prefix = 'biji_sc_'

    @staticmethod
    def is_share_code(sc: str) -> (bool, int, str):
        """
        判断是否是 合法共享码
        :return: (ok, uid, time)
        """
        ret = re.match('^biji_sc_(\\d+)_(\\d{16})$', sc)
        if not ret:
            return False, -1, ''
        return True, int(ret.group(1)), ret.group(2)

    def __init__(self):
        super(ShareCodeDao, self).__init__()

    def addShareCode(self, uid: int, dids: List[int], ex: int) -> str:
        """
        :param: uid 用户 id
        :param: dids 文档 id 列表
        :return: 分享码 '' for error
        """
        now = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-4]  # 2019111919004491 (16)
        uuid = '{}_{}'.format(uid, now)
        sc = self.sc_prefix + uuid  # biji_sc_23_2019111919004491
        dids = [did for did in json.dumps(dids) if DocumentDao().queryDocumentById(uid, did) is not None]
        if len(dids) == 0:
            return ''
        ok = self.db.set(name=sc, value=dids, ex=ex)
        return sc if ok else ''

    def getShareContent(self, sc: str) -> List[int]:
        """
        读取 分享码对应的文档编号集
        :return: (uid, [])
        """
        content = self.db.get(name=sc)  # biji_sc_23_2019111919004491
        return json.loads(content)

    def getUserShareCodes(self, uid: int) -> List[str]:
        """
        获取用户所有的共享码
        """
        pattern = f'{self.sc_prefix}{uid}_*'
        values = self.db.keys(pattern=pattern)
        return [v.decode('utf-8') for v in values]

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


'''
{
    "code": 200,
    "message": "Success",
    "data": [
        "biji_sc_1_2019111922214497",
        "biji_sc_1_2019111922270139",
        "biji_sc_1_2019111922272287",
        "biji_sc_1_2019111922271437",
        "biji_sc_1_2019111922242887"
    ]
}




'''