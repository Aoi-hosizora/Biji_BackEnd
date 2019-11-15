from typing import List, Optional

from app.database.DbErrorType import DbErrorType
from app.database.MySQLHelper import MySQLHelper
from app.model.po.DocumentClass import DocumentClass, DEF_DOC_CLASS


class DocumentClassDao(MySQLHelper):
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
                    {self.col_name} VARCHAR(100) NOT NULL UNIQUE,
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

    def queryAllDocumentClasses(self, uid: int) -> List[DocumentClass]:
        """
        查询所有文件分组
        """
        self.processDocumentClass(uid)  # 查询前处理

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
                returns.append(DocumentClass(cid=result[1], name=result[2]))
            except:
                pass

        cursor.close()
        return results

    def queryDocumentClassById(self, uid: int, cid: int) -> Optional[DocumentClass]:
        """
        根据 id 查询文件分组
        """
        self.processDocumentClass(uid)  # 查询前处理

        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_user}, {self.col_id}, {self.col_name}
            FROM {self.tbl_name}
            WHERE {self.col_user} = {uid} AND {self.col_id} = {cid}
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return DocumentClass(cid=result[1], name=result[2])
        except:
            return None
        finally:
            cursor.close()

    def queryDocumentClassByName(self, uid: int, name: str) -> Optional[DocumentClass]:
        """
        根据 name 查询文件分组
        """
        self.processDocumentClass(uid)  # 查询前处理

        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_user}, {self.col_id}, {self.col_name}
            FROM {self.tbl_name}
            WHERE {self.col_user} = {uid} AND {self.col_name} = '{name}'
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return DocumentClass(cid=result[1], name=result[2])
        except:
            return None
        finally:
            cursor.close()

    def queryDefaultDocumentClass(self, uid: int) -> DocumentClass:
        """
        查询默认分组
        """
        return self.queryDocumentClassByName(uid, DEF_DOC_CLASS.name)

    #######################################################################################################################

    def insertDocumentClass(self, uid: int, docClass: DocumentClass) -> DbErrorType:
        """
        插入新分组
        :return: SUCCESS | FOUNDED | FAILED | DUPLICATE
        """
        if self.queryDocumentClassById(uid, docClass.id) is not None:  # 已存在
            return DbErrorType.FOUNDED
        if self.queryDocumentClassByName(uid, docClass.name) is not None:  # 重复
            return DbErrorType.DUPLICATE
        self.processDocumentClass(uid)  # 插入前处理

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {self.tbl_name} ({self.col_user}, {self.col_id}, {self.col_name})
                VALUES ({uid}, {docClass.id}, '{docClass.name}')
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbErrorType.FAILED
            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()
            cursor.close()

    def updateDocumentClass(self, uid: int, docClass: DocumentClass) -> DbErrorType:
        """
        更新分组 (name)
        :return: SUCCESS | NOT_FOUND | DEFAULT | FAILED | DUPLICATE
        """
        if self.queryDocumentClassById(uid, docClass.id) is None:  # 不存在
            return DbErrorType.NOT_FOUND
        if self.queryDocumentClassByName(uid, docClass.name) is not None:  # 重复
            return DbErrorType.DUPLICATE
        self.processDocumentClass(uid)  # 更新前处理

        # 修改默认分组名
        defClass = self.queryDefaultDocumentClass(uid)
        if docClass.id == defClass.id and docClass.name != defClass:
            return DbErrorType.DEFAULT

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
                return DbErrorType.FAILED
            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()
            cursor.close()

    def deleteDocumentClass(self, uid: int, cid: int) -> DbErrorType:
        """
        删除一个分组
        :return: SUCCESS | NOT_FOUND | DEFAULT | FAILED
        """
        if self.queryDocumentClassById(uid, cid) is None:  # 不存在
            return DbErrorType.NOT_FOUND

        # 删除默认分组
        if cid == self.queryDefaultDocumentClass(uid).id:
            return DbErrorType.DEFAULT

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_id} = {cid}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbErrorType.FAILED

            self.processDocumentClass(uid)  # 删除后处理
            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()
            cursor.close()

    ####################################################################################

    def processDocumentClass(self, uid: int):
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

        def insert(docClass: DocumentClass):
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
