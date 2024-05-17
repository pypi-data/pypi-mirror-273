from typing import Any, List
from popoll_backend.model import Payload
from popoll_backend.model.db.user import User
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user_instruments import UserInstruments


class UserOut(Payload):
    
    def __init__(self, user: User, instruments: Instrument, user_instruments: List[UserInstruments]):
        self.user = user
        self.main_instrument: Instrument = [self.toDict(instruments)[i.instrument_id] for i in user_instruments if i.user_id == user.id and i.is_main][0]
        self.instruments: List[Instrument] = [self.toDict(instruments)[i.instrument_id] for i in user_instruments if i.user_id == user.id and not i.is_main]