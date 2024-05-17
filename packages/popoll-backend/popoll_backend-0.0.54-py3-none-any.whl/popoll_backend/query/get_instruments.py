import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.payload.instruments_payload import InstrumentsPayload
from popoll_backend.query import Query


class GetInstruments(Query):
    
    instruments: List[Instrument]
    
    def __init__(self, poll: str):
        super().__init__(poll)
    
    def process(self, cursor: sqlite3.Cursor):
        self.instruments = [Instrument(row) for row in cursor.execute('SELECT * from instruments.instruments').fetchall()]
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return InstrumentsPayload(self.instruments)