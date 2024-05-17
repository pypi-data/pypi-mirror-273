from typing import List, Optional
from popoll_backend.model.db.answer import Answer
from popoll_backend.model.db.date import Date
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model import Payload
from popoll_backend.model.payload.user import UserOut

class _UserDateOutput():
    
    def __init__(self, user: UserOut, date: Date, answers: List[Answer]):
        self.date: Date = date
        _ans = [a for a in answers if a.user_id == user.user.id and a.date_id == date.id]
        self.answer: Optional[Answer] = _ans[0] if len(_ans) > 0 else None
        

class UserPayload(Payload):
    
    def __init__(self, user: UserOut, answers: List[Answer], dates: List[Date]):
        self.user: UserOut = user
        self.dates: List[_UserDateOutput] = [_UserDateOutput(user, date, answers) for date in dates]