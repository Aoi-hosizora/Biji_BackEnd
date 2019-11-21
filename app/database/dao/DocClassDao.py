import os
from typing import List, Optional, Union

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper
from app.model.po.DocClass import DocClass, DEF_DOC_CLASS

tbl_name = "tbl_doc_class"

col_user = "dc_user"
col_id = "dc_id"
col_name = "dc_name"


class DocClassDao(MySQLHelper):

    def __init__(self):
        super().__init__()

    def create_tbl(self) -> bool:
        """
        判断是否存在并建表
        """
        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {tbl_name} (
                    {col_user} INT NOT NULL,
                    {col_id} INT PRIMARY KEY AUTO_INCREMENT,
                    {col_name} VARCHAR({Config.FMT_DOCCLASS_NAME_MAX}) NOT NULL UNIQUE
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()
        return True

    def queryAllDocClasses(self, uid: int) -> List[DocClass]:
        """
        查询所有文件分组
        """
        self.processDocClass(uid)  # 查询前处理

        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {col_user}, {col_id}, {col_name}
            FROM {tbl_name} WHERE {col_user} = {uid}
        ''')

        returns = []
        results = cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                returns.append(DocClass(cid=result[1], name=result[2]))
            except:
                pass

        cursor.close()
        return returns

    def queryDocClassByIdOrName(self, uid: int, cid_name: Union[int, str]) -> Optional[DocClass]:
        """
        根据 id 查询文件分组
        """
        self.processDocClass(uid)  # 查询前处理

        cursor = self.db.cursor()
        if isinstance(cid_name, int):
            cursor.execute(f'''
                SELECT {col_user}, {col_id}, {col_name}
                FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_id} = {cid_name}
            ''')
        else:
            cursor.execute(f'''
                SELECT {col_user}, {col_id}, {col_name}
                FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_name} = '{cid_name}'
            ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return DocClass(cid=result[1], name=result[2])
        except:
            return None
        finally:
            cursor.close()

    def queryDefaultDocClass(self, uid: int) -> DocClass:
        """
        查询默认分组
        """
        return self.queryDocClassByIdOrName(uid, cid_name=str(DEF_DOC_CLASS.name))

    #######################################################################################################################

    def insertDocClass(self, uid: int, docClass: DocClass) -> (DbStatusType, DocClass):
        """
        插入新分组 (name) SUCCESS | FOUNDED | FAILED | DUPLICATE
        """
        if self.queryDocClassByIdOrName(uid, cid_name=docClass.id) is not None:  # 已存在
            return DbStatusType.FOUNDED, None
        if self.queryDocClassByIdOrName(uid, cid_name=docClass.name) is not None:  # 重复
            return DbStatusType.DUPLICATE, None

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {tbl_name} ({col_user}, {col_name})
                VALUES ({uid}, '{docClass.name}')
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None
            return DbStatusType.SUCCESS, self.queryDocClassByIdOrName(uid, cursor.lastrowid)
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def updateDocClass(self, uid: int, docClass: DocClass) -> (DbStatusType, DocClass):
        """
        更新分组 (name) SUCCESS | NOT_FOUND | DEFAULT | FAILED | DUPLICATE
        """
        sameIdClass = self.queryDocClassByIdOrName(uid, docClass.id)
        if not sameIdClass:  # 不存在
            return DbStatusType.NOT_FOUND, None

        # 修改默认分组名
        if docClass.id == self.queryDefaultDocClass(uid).id:
            return DbStatusType.DEFAULT, None

        sameNameClass = self.queryDocClassByIdOrName(uid, docClass.name)
        if sameNameClass and docClass.id != sameNameClass.id:  # 重复
            return DbStatusType.DUPLICATE, None
        # 沒更新
        if docClass.name == sameIdClass.name:
            return DbStatusType.SUCCESS, sameIdClass

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                UPDATE {tbl_name} 
                SET {col_name} = '{docClass.name}'
                WHERE {col_user} = {uid} AND {col_id} = {docClass.id}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None

            self.db.commit()  # !!!
            self.processDocClass(uid)  # 更新后处理
            return DbStatusType.SUCCESS, self.queryDocClassByIdOrName(uid, int(docClass.id))
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def deleteDocClass(self, uid: int, cid: int, toDefault: bool) -> DbStatusType:
        """
        删除一个分组 SUCCESS | NOT_FOUND | DEFAULT | FAILED
        對應修改筆記
        """
        from app.database.dao import DocumentDao

        if self.queryDocClassByIdOrName(uid, cid) is None:  # 不存在
            return DbStatusType.NOT_FOUND

        # 删除默认分组
        def_class = self.queryDefaultDocClass(uid)
        if cid == def_class.id:
            return DbStatusType.DEFAULT

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            # 對應文档
            cursor.execute(f'''
                SELECT COUNT(*) FROM {DocumentDao.tbl_name} 
                WHERE {DocumentDao.col_user} = {uid} AND {DocumentDao.col_class_id} = {cid}
            ''')
            doc_len = cursor.fetchone()[0]

            if doc_len != 0:  # 有对应
                if toDefault:  # 修改為默認
                    cursor.execute(f'''
                        UPDATE {DocumentDao.tbl_name}
                        SET {DocumentDao.col_class_id} = {def_class.id}
                        WHERE {DocumentDao.col_user} = {uid} AND {DocumentDao.col_class_id} = {cid}
                    ''')
                    if cursor.rowcount == 0:
                        self.db.rollback()
                        return DbStatusType.FAILED
                else:  # 刪除
                    cursor.execute(f'''
                        SELECT {DocumentDao.col_uuid} FROM {DocumentDao.tbl_name}
                        WHERE {DocumentDao.col_class_id} = {cid}
                    ''')
                    uuids = cursor.fetchall()
                    uuids = [uuid[0] for uuid in uuids]
                    cursor.execute(f'''
                        DELETE FROM {DocumentDao.tbl_name}
                        WHERE {DocumentDao.col_user} = {uid} AND {DocumentDao.col_class_id} = {cid}
                    ''')
                    if cursor.rowcount == 0:
                        self.db.rollback()
                        return DbStatusType.FAILED
                    else:  # 删除文件
                        for uuid in uuids:
                            server_filepath = f'{Config.UPLOAD_DOC_FOLDER}/{uid}/{uuid}'
                            if os.path.exists(server_filepath):
                                os.remove(server_filepath)

            # 删除分组s
            cursor.execute(f'''
                DELETE FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_id} = {cid}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED

            self.db.commit()  # !!!
            self.processDocClass(uid)  # 删除后处理
            return DbStatusType.SUCCESS
        except:
            self.db.rollback()
            return DbStatusType.FAILED
        finally:
            self.db.commit()
            cursor.close()

    ####################################################################################

    def processDocClass(self, uid: int):
        """
        操作前后 处理默认分组
        """

        # 使用 Raw Json 防止递归
        def query(name: str) -> bool:
            cursor = self.db.cursor()
            cursor.execute(f'''
                SELECT * FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_name} = '{name}'
            ''')
            count = cursor.rowcount
            cursor.close()
            return count != 0

        def insert(docClass: DocClass):
            cursor = self.db.cursor()
            # noinspection PyBroadException
            try:
                cursor.execute(f'''
                    INSERT INTO {tbl_name} ({col_user}, {col_id}, {col_name})
                    VALUES ({uid}, {docClass.id}, '{docClass.name}')
                ''')
            except:
                self.db.rollback()
            finally:
                self.db.commit()
                cursor.close()

        # 插入默认分组
        if not query(DEF_DOC_CLASS.name):
            insert(DEF_DOC_CLASS)
