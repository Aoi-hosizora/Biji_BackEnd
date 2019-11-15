from typing import List, Optional

from app.database.DbErrorType import DbErrorType
from app.database.MySQLHelper import MySQLHelper
from app.database.dao.DocumentClassDao import DocumentClassDao

from app.model.po.Document import Document


class DocumentDao(MySQLHelper):
    tbl_name = "tbl_document"

    col_user = "d_user"
    col_id = "d_id"
    col_filename = "d_filename"
    col_class_id = "d_class_id"

    def __init__(self):
        super().__init__()

    def create_tbl(self) -> bool:
        """
        判断表是否存在并且建表
        """
        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.tbl_name} (
                    {self.col_user} INT NOT NULL,
                    {self.col_id} INT AUTO_INCREMENT,
                    {self.col_filename} VARCHAR(200) NOT NULL,
                    {self.col_class_id} INT NOT NULL,
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

    def queryAllDocuments(self, uid: int) -> List[Document]:
        """
        查询所有文件
        """
        return self.queryDocumentsByClassId(uid, -1)

    def queryDocumentsByClassId(self, uid: int, cid: int) -> List[Document]:
        """
        根据分组查询文件
        :param uid: 用户id
        :param cid: 所有分组为 -1
        """
        cursor = self.db.cursor()
        if cid == -1:
            cursor.execute(f'''
                SELECT {self.col_user}, {self.col_id}, {self.col_filename}, {self.col_class_id}
                FROM {self.tbl_name} 
                WHERE {self.col_user} = {uid}
            ''')
        else:
            cursor.execute(f'''
                SELECT {self.col_user}, {self.col_id}, {self.col_filename}, {self.col_class_id}
                FROM {self.tbl_name} 
                WHERE {self.col_user} = {uid} AND {self.col_class_id} = {cid}
            ''')

        returns = []
        results = cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                class_id: int = int(result[3])
                docClass = DocumentClassDao().queryDocumentClassById(uid, class_id)
                if docClass is None:
                    docClass = DocumentClassDao().queryDefaultDocumentClass(uid)
                returns.append(Document(did=result[1], filename=result[2], docClass=docClass))
            except:
                pass
        cursor.close()
        return returns

    def queryDocumentById(self, uid: int, did: int) -> Optional[Document]:
        """
        根据 id 查询文件
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_user}, {self.col_id}, {self.col_filename}, {self.col_class_id}
            FROM {self.tbl_name}
            WHERE {self.col_user} = {uid} AND {self.col_id} = {did}
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            class_id: int = int(result[3])
            docClass = DocumentClassDao().queryDocumentClassById(uid, class_id)
            if docClass is None:
                docClass = DocumentClassDao().queryDefaultDocumentClass(uid)
            return Document(did=result[1], filename=result[2], docClass=docClass)
        except:
            return None
        finally:
            cursor.close()

    #######################################################################################################################

    def insertDocument(self, uid: int, document: Document) -> DbErrorType:
        """
        插入新文档
        :return: SUCCESS | FOUNDED | FAILED
        """
        if self.queryDocumentById(uid, document.id) is not None:  # 已存在
            return DbErrorType.FOUNDED

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {self.tbl_name} (
                    {self.col_user}, {self.col_id}, {self.col_filename}, {self.col_class_id}
                )
                VALUES ({uid}, {document.id}, '{document.filename}', {document.docClass.id}) 
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

    def updateDocument(self, uid: int, document: Document) -> DbErrorType:
        """
        更新文档 (docClass)
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        if self.queryDocumentById(uid, document.id) is None:
            return DbErrorType.NOT_FOUND

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                UPDATE {self.tbl_name} 
                WHERE {self.col_user} = {uid} AND {self.col_id} = {document.id}
                SET {self.col_class_id} = {document.docClass.id}
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

    def deleteDocument(self, uid: int, did: int) -> DbErrorType:
        """
        删除一项文件
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        if self.queryDocumentById(uid, did) is None:  # 不存在
            return DbErrorType.NOT_FOUND

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_id} = {did}
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
