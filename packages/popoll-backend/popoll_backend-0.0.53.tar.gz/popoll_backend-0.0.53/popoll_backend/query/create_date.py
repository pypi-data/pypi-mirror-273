import datetime
import sqlite3
from typing import Optional

from popoll_backend.model import Payload
from popoll_backend.query import Query
from popoll_backend.query.get_date import GetDate


class CreateDate(Query):
    
    title: str
    date: datetime.date
    time: Optional[datetime.time]
    end_time: Optional[datetime.time]
    
    id: int
    
    def __init__(self, poll: str, title: str, date: datetime.date, time: Optional[datetime.time], end_time: Optional[datetime.time]):
        super().__init__(poll)
        self.title = title
        self.date = date
        self.time = time
        self.end_time = end_time
    
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('INSERT INTO dates(title, date, time, end_time) VALUES (?, ?, ?, ?)', (self.title, self.date, self.time, self.end_time))
        self.id = cursor.lastrowid
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return GetDate(self.poll, self.id, False).run(cursor)