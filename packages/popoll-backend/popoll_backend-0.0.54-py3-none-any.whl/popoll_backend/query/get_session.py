import sqlite3

import flask

from popoll_backend.model import Payload
from popoll_backend.model.db.session import Session
from popoll_backend.model.payload.id_payload import IdPayload
from popoll_backend.query import Query


class GetSession(Query):
    
    id: int
    
    session: Session
    
    def __init__(self, poll: str, id: str):
        super().__init__(poll)
        self.id = id

    def process(self, cursor: sqlite3.Cursor):
        pass

    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        res = cursor.execute('SELECT * FROM sessions WHERE session_id=?', (self.id,)).fetchall()
        if len(res) == 0:
            flask.abort(404, f'Object of type [Session] and session_id [{self.id}] has not been found.')
        return Session(res[-1])