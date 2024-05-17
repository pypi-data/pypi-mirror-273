import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.db.answer import Answer
from popoll_backend.query import Query


class GetAnswer(Query):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id

    def process(self, cursor: sqlite3.Cursor):
        pass
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return self.selectItem(cursor, 'SELECT * from answers where id=?', self.id, Answer)