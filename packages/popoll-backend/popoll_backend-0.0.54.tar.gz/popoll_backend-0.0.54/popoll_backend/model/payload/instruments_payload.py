from typing import List
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model import Payload


class InstrumentsPayload(Payload):
    
    def __init__(self, instruments: List[Instrument]):
        self.instruments: List[Instrument] = instruments