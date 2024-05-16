from popoll_backend.model import Payload

class IdPayload(Payload):
    
    def __init__(self, id: int):
        self.id: int = id
    
    