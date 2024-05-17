from popoll_backend.model import Payload
from popoll_backend.model.db.instrument import Instrument


class InstrumentPayload(Payload):
    
    def __init__(self, instrument: Instrument, is_used: bool):
        self.instrument = instrument
        self.is_used = is_used