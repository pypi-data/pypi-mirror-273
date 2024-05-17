import sqlite3
from typing import List

import flask

from popoll_backend.model import Payload
from popoll_backend.model.db.answer import Answer
from popoll_backend.model.db.date import Date
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.option import Option
from popoll_backend.model.db.session import Session
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.id_payload import IdPayload
from popoll_backend.query import Query


class CreatePoll(Query):
    
    fail_if_db_exists: bool = True
    fail_if_db_not_exists: bool = False
    
    name: str
    instruments: List[str]
    color: str
    
    def __init__(self, poll:str, name: str, instruments: List[str], color: str):
        super().__init__(poll)
        self.name = name
        self.instruments = instruments
        self.color = color
    
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute(Option.create_table())
        cursor.execute('INSERT INTO options(name, color) values(?, ?)', (self.name, self.color))
        # cursor.execute(Instrument.create_table())
        # cursor.executemany('INSERT INTO instruments(name) values(?)', [(d,) for d in self.instruments])
        cursor.execute(Date.create_table())
        cursor.execute(User.create_table())
        cursor.execute(Answer.create_table())
        cursor.execute(UserInstruments.create_table())
        cursor.execute(Session.create_table())
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return IdPayload(0)