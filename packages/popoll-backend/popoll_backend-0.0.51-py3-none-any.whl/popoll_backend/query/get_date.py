import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.db.answer import Answer
from popoll_backend.model.db.date import Date
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.date_payload import DatePayload
from popoll_backend.query import Query
from popoll_backend.query.get_instruments import GetInstruments
from popoll_backend.query.get_users import GetUsers


class GetDate(Query):
    
    id: int
    details: bool
    
    date: Date
    answers: List[Answer]
    users: List[User]
    instruments: List[Instrument]
    user_instruments: List[UserInstruments]
    
    def __init__(self, poll: str, id: int, details: bool = False):
        super().__init__(poll)
        self.id = id
        self.details = details

    def process(self, cursor: sqlite3.Cursor):
        self.date = self.selectItem(cursor, 'SELECT * from dates where id=?', self.id, Date)
        if self.details:
            self.answers: List[Answer] = [Answer(row) for row in cursor.execute('SELECT * from answers where date_id=?', (self.id,)).fetchall()]
            self.users: List[User] = GetUsers(self.poll).run(cursor).users
            self.instruments: List[Instrument] = GetInstruments(self.poll).run(cursor).instruments
            self.user_instruments: List[UserInstruments] = [UserInstruments(row) for row in cursor.execute('SELECT * FROM user_instruments').fetchall()]

    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        if not self.details:
            return self.date
        return DatePayload(self.date, self.answers, self.users, self.instruments, self.user_instruments)