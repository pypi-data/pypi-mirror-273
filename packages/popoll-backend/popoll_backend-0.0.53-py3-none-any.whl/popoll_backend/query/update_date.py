import datetime
import sqlite3
from typing import Optional

from popoll_backend.model import Payload
from popoll_backend.query import Query
from popoll_backend.query.get_date import GetDate


class UpdateDate(Query):
    
    id: int
    title: str
    date: datetime.date
    time: Optional[datetime.time]
    end_time: Optional[datetime.time]
    
    def __init__(self, poll: str, id: int, title: str, date: datetime.date, time: Optional[datetime.time], end_time: Optional[datetime.time]):
        super().__init__(poll)
        self.id = id
        self.title = title
        self.date = date
        self.time = time
        self.end_time = end_time
        
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('UPDATE dates SET title=?, date=?, time=?, end_time=? WHERE id=?', (self.title, self.date, self.time, self.end_time, self.id))
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return GetDate(self.poll, self.id, False).run(cursor)