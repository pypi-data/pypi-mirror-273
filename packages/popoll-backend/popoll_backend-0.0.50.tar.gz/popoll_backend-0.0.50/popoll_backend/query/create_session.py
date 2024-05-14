import datetime
import sqlite3

from popoll_backend.model import Payload
from popoll_backend.query import Query
from popoll_backend.query.get_session import GetSession


class CreateSession(Query):
    
    id: int
    
    def __init__(self, poll: str, id: str, user_id: int):
        super().__init__(poll)
        self.id = id
        self.user_id = user_id

    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('DELETE FROM sessions WHERE session_id=?', (self.id,))
        cursor.execute('INSERT INTO sessions(session_id, user_id, datetime) VALUES(?, ?, ?)', (self.id, self.user_id, datetime.datetime.now().isoformat(sep='T', timespec='auto')))

    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return GetSession(self.poll, self.id).run(cursor)