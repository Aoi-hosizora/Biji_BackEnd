from typing import List, Optional, Union

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper
from app.model.po.DocClass import DocClass, DEF_DOC_CLASS


class DocClassDao(MySQLHelper):
    tbl_name = "tbl_doc_class"

    col_user = "dc_user"
    col_id = "dc_id"
    col_name = "dc_name"

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
                CREATE TABLE IF NOT EXISTS {self.tbl_name} (
                    {self.col_user} INT NOT NULL,
                    {self.col_id} INT AUTO_INCREMENT,
                    {self.col_name} VARCHAR({Config.FMT_DOCCLASS_NAME_MAX}) NOT NULL UNIQUE,
                    PRIMARY KEY ({self.col_user}, {self.col_id})
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
            SELECT {self.col_user}, {self.col_id}, {self.col_name}
            FROM {self.tbl_name} WHERE {self.col_user} = {uid}
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
        return results

    def queryDocClassByIdOrName(self, uid: int, cid_name: Union[int, str]) -> Optional[DocClass]:
        """
        根据 id 查询文件分组
        """
        self.processDocClass(uid)  # 查询前处理

        cursor = self.db.cursor()
        if isinstance(cid_name, int):
            cursor.execute(f'''
                SELECT {self.col_user}, {self.col_id}, {self.col_name}
                FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_id} = {cid_name}
            ''')
        else:
            cursor.execute(f'''
                SELECT {self.col_user}, {self.col_id}, {self.col_name}
                FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_name} = '{cid_name}'
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
        return self.queryDocClassByIdOrName(uid, cid_name=DEF_DOC_CLASS.name)

    #######################################################################################################################

    def insertDocClass(self, uid: int, docClass: DocClass) -> (DbStatusType, DocClass):
        """
        插入新分组 (name) SUCCESS | FOUNDED | FAILED | DUPLICATE
        """
        if self.queryDocClassByIdOrName(uid, cid_name=docClass.id) is not None:  # 已存在
            return DbStatusType.FOUNDED, None
        if self.queryDocClassByIdOrName(uid, cid_name=docClass.name) is not None:  # 重复
            return DbStatusType.DUPLICATE, None
        self.processDocClass(uid)  # 插入前处理

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {self.tbl_name} ({self.col_user}, {self.col_name})
                VALUES ({uid}, '{docClass.name}')
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None

            cursor.execute(f'''SELECT MAX({self.col_id} FROM {self.tbl_name}''')
            new_docClass_id = int(cursor.fetchone()[0])
            new_docClass = self.queryDocClassByIdOrName(uid, new_docClass_id)
            return DbStatusType.SUCCESS, new_docClass
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
        if self.queryDocClassByIdOrName(uid, docClass.id) is None:  # 不存在
            return DbStatusType.NOT_FOUND, None
        if self.queryDocClassByIdOrName(uid, docClass.name) is not None:  # 重复
            return DbStatusType.DUPLICATE, None
        self.processDocClass(uid)  # 更新前处理

        # 修改默认分组名
        defClass = self.queryDefaultDocClass(uid)
        if docClass.id == defClass.id and docClass.name != defClass:
            return DbStatusType.DEFAULT, None

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                UPDATE {self.tbl_name} 
                WHERE {self.col_user} = {uid} AND {self.col_id} = {docClass.id}
                SET {self.col_name} = '{docClass.name}'
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None

            cursor.execute(f'''SELECT MAX({self.col_id} FROM {self.tbl_name}''')
            new_docclass_id = int(cursor.fetchone()[0])
            new_docclass = self.queryDocClassByIdOrName(uid, new_docclass_id)
            return DbStatusType.SUCCESS, new_docclass
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def deleteDocClass(self, uid: int, cid: int) -> DbStatusType:
        """
        删除一个分组
        :return: SUCCESS | NOT_FOUND | DEFAULT | FAILED
        """
        if self.queryDocClassByIdOrName(uid, cid) is None:  # 不存在
            return DbStatusType.NOT_FOUND

        # 删除默认分组
        if cid == self.queryDefaultDocClass(uid).id:
            return DbStatusType.DEFAULT

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_id} = {cid}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED

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
                SELECT * FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_name} = {name}
            ''')
            return cursor.rowcount != 0

        def insert(docClass: DocClass):
            cursor = self.db.cursor()
            # noinspection PyBroadException
            try:
                cursor.execute(f'''
                    INSERT INTO {self.tbl_name} ({self.col_user}, {self.col_id}, {self.col_name}
                    VALUES ({uid}, {docClass.id}, '{docClass.name}')
                ''')
            except:
                self.db.rollback()
            finally:
                self.db.commit()
                cursor.close()

        # 插入默认分组
        if query(DEF_DOC_CLASS.name) is None:
            insert(DEF_DOC_CLASS)
