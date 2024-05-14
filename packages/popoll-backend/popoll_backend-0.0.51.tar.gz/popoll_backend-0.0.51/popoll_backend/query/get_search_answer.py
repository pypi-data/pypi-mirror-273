import sqlite3
from typing import List

import flask

from popoll_backend.model import Payload
from popoll_backend.model.db.answer import Answer
from popoll_backend.query import Query


class GetSearchAnswer(Query):
    
    userId: int
    dateId: int
    
    def __init__(self, poll: str, userId: int, dateId: int):
        super().__init__(poll)
        self.userId = userId
        self.dateId = dateId

    def process(self, cursor: sqlite3.Cursor):
        pass
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        res = cursor.execute('SELECT * FROM answers WHERE user_id=? AND date_id=?', (self.userId, self.dateId)).fetchall()
        if (len(res) == 0):
            flask.abort(404, f'Object of type [Answer] and matching user_id=[{self.userId}] and date_id=[{self.dateId}] has not been found.')
        return Answer(res[0])