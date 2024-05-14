import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.db.option import Option
from popoll_backend.query import Query


class GetPoll(Query):
    
    def __init__(self, poll: str):
        super().__init__(poll)

    def process(self, cursor: sqlite3.Cursor):
        pass
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        res = cursor.execute('SELECT * FROM options').fetchone()
        return Option(res)