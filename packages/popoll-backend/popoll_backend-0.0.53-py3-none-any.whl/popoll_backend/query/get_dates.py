import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.db.date import Date
from popoll_backend.model.payload.dates_payload import DatesPayload
from popoll_backend.query import Query


class GetDates(Query):
    
    dates: List[Date]
    
    def __init__(self, poll: str):
        super().__init__(poll)

    def process(self, cursor: sqlite3.Cursor):
        self.dates = [Date(row) for row in cursor.execute('SELECT * FROM dates ORDER BY date, time').fetchall()]
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return DatesPayload(self.dates)