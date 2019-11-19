from typing import List, Optional

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper
from app.database.dao.DocClassDao import DocClassDao
from app.model.po.DocClass import DocClass

from app.model.po.Document import Document


class DocumentDao(MySQLHelper):
    tbl_name = "tbl_document"

    col_user = "d_user"
    col_id = "d_id"
    col_filename = "d_filename"
    col_uuid = "d_uuid_name"
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
                    {self.col_id} INT PRIMARY KEY AUTO_INCREMENT,
                    {self.col_filename} TEXT NOT NULL,
                    {self.col_uuid} VARCHAR({Config.FMT_DOCUMENT_UUID_LEN}) NOT NULL,
                    {self.col_class_id} INT NOT NULL
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
                SELECT {self.col_user}, {self.col_id}, {self.col_filename}, {self.col_class_id}, {self.col_uuid}
                FROM {self.tbl_name} 
                WHERE {self.col_user} = {uid}
            ''')
        else:
            cursor.execute(f'''
                SELECT {self.col_user}, {self.col_id}, {self.col_filename}, {self.col_class_id}, {self.col_uuid}
                FROM {self.tbl_name} 
                WHERE {self.col_user} = {uid} AND {self.col_class_id} = {cid}
            ''')

        returns = []
        results = cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                docClass = DocClassDao().queryDocClassByIdOrName(uid, result[3])
                if docClass is None:
                    docClass = DocClassDao().queryDefaultDocClass(uid)
                returns.append(Document(did=result[1], filename=result[2], docClass=docClass, uuid=result[4]))
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
            SELECT {self.col_user}, {self.col_id}, {self.col_filename}, {self.col_class_id}, {self.col_uuid}
            FROM {self.tbl_name}
            WHERE {self.col_user} = {uid} AND {self.col_id} = {did}
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            docClass = DocClassDao().queryDocClassByIdOrName(uid, result[3])
            if docClass is None:
                docClass = DocClassDao().queryDefaultDocClass(uid)
            return Document(did=result[1], filename=result[2], docClass=docClass, uuid=result[4])
        except:
            return None
        finally:
            cursor.close()

    def queryDocumentsByIds(self, uid: int, ids: List[int]) -> List[Document]:
        """
        根据 ids 查询 Document[]
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_user}, {self.col_id}, {self.col_filename}, {self.col_class_id}, {self.col_uuid}
            FROM {self.tbl_name}
            WHERE {self.col_user} = {uid} AND {self.col_id} IN ({', '.join([str(did) for did in ids])})
        ''')
        result = cursor.fetchall()
        returns: List[Document] = []
        for ret in result:
            # noinspection PyBroadException
            try:
                docClass = DocClassDao().queryDocClassByIdOrName(uid, ret[3])
                if docClass is None:
                    docClass = DocClassDao().queryDefaultDocClass(uid)
                returns.append(Document(did=ret[1], filename=ret[2], docClass=docClass, uuid=ret[4]))
            except:
                pass
        cursor.close()
        return returns

    def queryUuidByIds(self, uid: int, ids: List[int]) -> List[str]:
        """
        根据 ids 查询 uuid[]
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_uuid} FROM {self.tbl_name}
            WHERE {self.col_user} = {uid} AND {self.col_id} IN ({', '.join([str(did) for did in ids])})
        ''')
        result = cursor.fetchall()
        returns: List[str] = []
        for ret in result:
            # noinspection PyBroadException
            try:
                returns.append(ret[0])
            except:
                pass
        cursor.close()
        return returns

    #######################################################################################################################

    def insertDocument(self, uid: int, document: Document) -> (DbStatusType, Document):
        """
        插入新文档 (filename, uuid, docclass) SUCCESS | FOUNDED | FAILED
        """
        if self.queryDocumentById(uid, document.id):  # 已存在
            return DbStatusType.FOUNDED, None

        if not DocClassDao().queryDocClassByIdOrName(uid=uid, cid_name=document.docClass.id):  # 分组不存在
            document.docClass = DocClassDao().queryDefaultDocClass(uid=uid)

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {self.tbl_name} (
                    {self.col_user}, {self.col_filename}, {self.col_class_id}, {self.col_uuid}
                )
                VALUES ({uid}, '{document.filename}', {document.docClass.id}, '{document.uuid}') 
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None
            return DbStatusType.SUCCESS, self.queryDocumentById(uid, cursor.lastrowid)
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def updateDocument(self, uid: int, document: Document) -> (DbStatusType, Document):
        """
        更新文档 (filename, docClass) SUCCESS | NOT_FOUND | FAILED
        """
        sameIdDoc = self.queryDocumentById(uid, document.id)
        if not sameIdDoc:
            return DbStatusType.NOT_FOUND, None

        if not DocClassDao().queryDocClassByIdOrName(uid=uid, cid_name=document.docClass.id):  # 分组不存在
            document.docClass = DocClassDao().queryDefaultDocClass(uid=uid)

        # 沒更新
        if sameIdDoc.filename == document.filename and sameIdDoc.docClass.id == document.docClass.id:
            return DbStatusType.SUCCESS, sameIdDoc

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                UPDATE {self.tbl_name} 
                SET {self.col_class_id} = {document.docClass.id}, {self.col_filename} = '{document.filename}'
                WHERE {self.col_user} = {uid} AND {self.col_id} = {document.id}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None
            return DbStatusType.SUCCESS, self.queryDocumentById(uid, document.id)
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def deleteDocument(self, uid: int, did: int) -> DbStatusType:
        """
        删除一项文件 SUCCESS | NOT_FOUND | FAILED
        """
        if self.queryDocumentById(uid, did) is None:  # 不存在
            return DbStatusType.NOT_FOUND

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_id} = {did}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED
            return DbStatusType.SUCCESS
        except:
            self.db.rollback()
            return DbStatusType.FAILED
        finally:
            self.db.commit()
            cursor.close()
