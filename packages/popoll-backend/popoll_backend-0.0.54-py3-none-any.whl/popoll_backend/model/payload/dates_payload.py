from typing import List
from popoll_backend.model.db.date import Date
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model import Payload


class DatesPayload(Payload):
    
    def __init__(self, dates: List[Date]):
        self.dates: List[Date] = dates