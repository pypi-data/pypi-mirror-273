import sqlite3

from popoll_backend.model import Payload
from popoll_backend.model.payload.id_payload import IdPayload
from popoll_backend.query import Query


class CreateInstrument(Query):
    
    name: str
    instrument_id: int
    
    def __init__(self, poll, name: str):
        super().__init__(poll)
        self.name = name
        
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('INSERT INTO instruments.instruments(name) VALUES (?)', (self.name,))
        self.instrument_id = cursor.lastrowid
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return IdPayload(self.instrument_id)
