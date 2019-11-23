import json
import re
from typing import List
from datetime import datetime

from app.database.RedisHelper import RedisHelper
from app.database.dao.DocumentDao import DocumentDao
from app.model.po.Document import Document


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

    def addShareCode(self, uid: int, dids: List[int], ex: int) -> (str, List[Document]):
        """
        :param: uid 用户 id
        :param: dids 文档 id 列表
        :return: sc ('') & doc[] ([])
        """
        now = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-4]  # 2019111919004491 (16)
        uuid = '{}_{}'.format(uid, now)
        sc = self.sc_prefix + uuid  # biji_sc_23_2019111919004491

        # 传入空文档集
        if len(dids) == 0:
            return '', []

        # 共享的文档与id
        docs = [doc for doc in DocumentDao().queryDocumentsByIds(uid, dids) if doc]
        dids = [doc.id for doc in docs]  # 不管文件存不存在

        # 存在的文档集空
        if len(dids) == 0:
            return '', []

        ok = self.db.set(name=sc, value=json.dumps(dids), ex=ex)
        if ok:
            return sc, docs
        else:
            return '', docs

    def getShareContent(self, sc: str) -> List[int]:
        """
        读取 分享码对应的文档编号集
        :return: (uid, [])
        """
        content = self.db.get(name=sc)  # biji_sc_23_2019111919004491
        # noinspection PyBroadException
        try:
            return json.loads(content)
        except:
            return []

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
