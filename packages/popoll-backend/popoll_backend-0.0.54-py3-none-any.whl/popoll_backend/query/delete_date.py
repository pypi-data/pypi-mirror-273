import sqlite3
from popoll_backend.model import Payload
from popoll_backend.model.payload.id_payload import IdPayload
from popoll_backend.query import Query


class DeleteDate(Query):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id
    
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('DELETE FROM dates WHERE id=?', (self.id,))
    
    def buildResponse(self, _: sqlite3.Cursor) -> Payload:
        return IdPayload(self.id)
    