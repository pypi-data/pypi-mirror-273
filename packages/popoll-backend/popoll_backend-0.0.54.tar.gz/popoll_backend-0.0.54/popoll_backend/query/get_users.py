import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.user import UserOut
from popoll_backend.model.payload.users_payload import UsersPayload
from popoll_backend.model.payload.users_payload_details import UsersPayloadDetails
from popoll_backend.query import Query
from popoll_backend.query.get_instruments import GetInstruments


class GetUsers(Query):
    
    details: bool
    
    users: List[User]
    instruments: List[Instrument]
    user_instruments: List[UserInstruments]
    
    def __init__(self, poll: str, details: bool = False):
        super().__init__(poll)
        self.details = details
    
    def process(self, cursor: sqlite3.Cursor):
        self.users = [User(data) for data in cursor.execute('SELECT * from users ORDER BY name COLLATE NOCASE').fetchall()]       
        if self.details:
            self.instruments: List[Instrument] = GetInstruments(self.poll).run(cursor).instruments
            self.user_instruments: List[UserInstruments] = [UserInstruments(data) for data in cursor.execute('SELECT * from user_instruments').fetchall()]

    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        if not self.details:
            return UsersPayload(self.users)
        users_out = [UserOut(_user, self.instruments, self.user_instruments) for _user in self.users]    
        return UsersPayloadDetails(users_out)