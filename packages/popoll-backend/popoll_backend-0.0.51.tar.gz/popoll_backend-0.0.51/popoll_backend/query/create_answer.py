import sqlite3

import flask

from popoll_backend.model import Payload
from popoll_backend.query import Query
from popoll_backend.query.get_answer import GetAnswer


class CreateAnswer(Query):
    
    user_id: int
    date_id: int
    
    id: int
    
    def __init__(self, poll:str, user_id: int, date_id: int):
        super().__init__(poll)
        self.user_id = user_id
        self.date_id = date_id
    
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('INSERT INTO answers(user_id, date_id, response) VALUES (?, ?, ?)', (self.user_id, self.date_id, True))
        self.id = cursor.lastrowid
        
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return GetAnswer(self.poll, self.id).run(cursor)
    
    def error(self, e: sqlite3.Error):
        if isinstance(e, sqlite3.IntegrityError):
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                flask.abort(400, f'Answer for this user already exists. PUT should be triggered instead.')