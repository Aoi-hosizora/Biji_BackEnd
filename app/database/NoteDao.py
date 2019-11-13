from app.database.DbErrorType import DbErrorType
from app.database.DbHelper import DbHelper
from typing import List

from app.database.GroupDao import GroupDao
from app.module.note.Models.Note import Note


class NoteDao(DbHelper):
    tbl_name = "TBL_NOTE"

    col_username = "USERNAME"
    col_id = "ID"
    col_title = "TITLE"
    col_content = "CONTENT"
    col_group_id = "GROUP_ID"
    col_create_time = "CREATE_TIME"
    col_update_time = "UPDATE_TIME"

    def __init__(self):
        super().__init__()

    def createTbl(self) -> bool:
        """
        判断表是否存在，并且创建表
        """
        # noinspection PyBroadException
        try:
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.tbl_name} (
                    {self.col_username} VARCHAR(30) NOT NULL,
                    {self.col_id} INT NOT NULL,
                    {self.col_title} VARCHAR(100) NOT NULL,
                    {self.col_content} TEXT,
                    {self.col_group_id} INT NOT NULL,
                    {self.col_create_time} DATETIME NOT NULL,
                    {self.col_update_time} DATETIME NOT NULL,
                )
            ''')
            self.db.commit()
        except:
            self.db.rollback()
            self.db.commit()
            return False
        return True

    def queryAllNotes(self, username: str) -> List[Note]:
        """
        查询所有笔记
        """
        return self.queryAllNotesByGroupId(username, -1)

    def queryAllNotesByGroupId(self, username: str, group_id: int) -> List[Note]:
        """
        根据分组查询笔记
        :param username:
        :param group_id: 所有分组为 -1
        """
        if group_id == -1:
            self.cursor.execute(f'''
                SELECT {self.col_username}, {self.col_id}, {self.col_title}, {self.col_content}, {self.col_group_id}, {self.col_create_time}, {self.col_update_time}
                FROM {self.tbl_name} 
                WHERE {self.col_username} = '{username}'
            ''')
        else:
            self.cursor.execute(f'''
                SELECT {self.col_username}, {self.col_id}, {self.col_title}, {self.col_content}, {self.col_group_id}, {self.col_create_time}, {self.col_update_time}
                FROM {self.tbl_name} 
                WHERE {self.col_username} = '{username}' AND {self.col_group_id} = {group_id}
            ''')

        returns = []
        results = self.cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                group_id: int = int(result[4])
                group = GroupDao().queryUserOneGroup(username, group_id)
                if group is None:
                    group = GroupDao().queryDefaultGroup()
                note = Note(nid=result[1], title=result[2], content=result[3], group=group, create_time=result[5], update_time=result[6])
                returns.append(note)
            except:
                pass
        return returns

    def queryNoteById(self, username: str, nid: int) -> Note or None:
        """
        根据 nid 查询笔记
        :return: nullable
        """
        self.cursor.execute(f'''
            SELECT {self.col_username}, {self.col_id}, {self.col_title}, {self.col_content}, {self.col_group_id}, {self.col_create_time}, {self.col_update_time}
            FROM {self.tbl_name}
            WHERE {self.col_username} = '{username}' AND {self.col_id} = {nid}
        ''')
        result = self.cursor.fetchone()
        # noinspection PyBroadException
        try:
            group_id: int = int(result[4])
            group = GroupDao().queryUserOneGroup(username, group_id)
            if group is None:
                group = GroupDao().queryDefaultGroup()
            return Note(nid=result[1], title=result[2], content=result[3], group=group, create_time=result[5], update_time=result[6])
        except:
            return None

    def insertNote(self, username: str, note: Note) -> DbErrorType:
        """
        插入新笔记
        :return: SUCCESS | FOUNDED | FAILED
        """
        if self.queryNoteById(username, note.id) is not None:
            return DbErrorType.FOUNDED
        # noinspection PyBroadException
        try:
            self.cursor.execute(f'''
                INSERT INTO {self.tbl_name} (
                    {self.col_username}, {self.col_id}, {self.col_title}, {self.col_content}, {self.col_group_id}, {self.col_create_time}, {self.col_update_time}
                )
                VALUES (
                    '{username}', {note.id}, '{note.title}', '{note.content}', {note.group.id}, '{note.create_time}', '{note.update_time}'
                )
            ''')
            self.db.commit()

            if self.queryNoteById(username, note.id) is None:
                self.db.rollback()
                return DbErrorType.FAILED

            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()

    def updateNote(self, username: str, note: Note) -> DbErrorType:
        """
        更新笔记 除了 nid
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        if self.queryNoteById(username, note.id) is None:
            return DbErrorType.NOT_FOUND
        # noinspection PyBroadException
        try:
            self.cursor.execute(f'''
                UPDATE {self.tbl_name}
                SET {self.col_title} = '{note.title}', {self.col_content} = '{note.content}', {self.col_group_id} = {note.group.id},
                    {self.col_create_time} = '{note.create_time}', {self.col_update_time} = '{note.update_time}'
            ''')

            newNote = self.queryNoteById(username, note.id)
            if newNote.title != note.title or newNote.content != note.content or newNote.group.id != note.group.id \
                    or newNote.create_time != note.create_time or newNote.update_time != note.update_time:
                self.db.rollback()
                return DbErrorType.FAILED

            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()

    def deleteNote(self, username: str, nid: int) -> DbErrorType:
        """
        删除一条笔记
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        if self.queryNoteById(username, nid) is None:
            return DbErrorType.NOT_FOUND
        # noinspection PyBroadException
        try:
            self.cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_username} = '{username}' AND {self.col_id} = {nid}
            ''')

            if self.queryNoteById(username, nid) is not None:
                self.db.rollback()
                return DbErrorType.FAILED

            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()
