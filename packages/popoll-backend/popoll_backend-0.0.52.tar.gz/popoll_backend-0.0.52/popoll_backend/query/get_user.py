import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.db.answer import Answer
from popoll_backend.model.db.date import Date
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.user import UserOut
from popoll_backend.model.payload.user_payload import UserPayload
from popoll_backend.query import Query
from popoll_backend.query.get_instruments import GetInstruments


class GetUser(Query):
    
    id: int
    details: bool
    
    user: User
    instruments: List[Instrument]
    user_instruments: List[UserInstruments]
    answers: List[Answer]
    dates: List[Date]
    
    def __init__(self, poll: str, id: int, details: bool = False):
        super().__init__(poll)
        self.id = id
        self.details = details
    
    def process(self, cursor: sqlite3.Cursor):
        self.user = self.selectItem(cursor, 'SELECT * from users WHERE id=?', self.id, User)
        self.instruments: List[Instrument] = GetInstruments(self.poll).run(cursor).instruments
        self.user_instruments: List[UserInstruments] = [UserInstruments(data) for data in cursor.execute('SELECT * from user_instruments WHERE user_id=?', (self.id,)).fetchall()]
        if self.details:
            self.answers: List[Answer] = [Answer(data) for data in cursor.execute('SELECT * FROM answers WHERE user_id=?', (self.id,)).fetchall()]
            self.dates: List[Date] = [Date(data) for data in cursor.execute(f'SELECT * FROM dates ORDER BY date, time').fetchall()]
        
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        user_out: UserOut = UserOut(self.user, self.instruments, self.user_instruments)
        if not self.details:
            return user_out
        return UserPayload(user_out, self.answers, self.dates)
        
        
        