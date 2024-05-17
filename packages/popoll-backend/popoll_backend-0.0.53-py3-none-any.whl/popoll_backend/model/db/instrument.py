from typing import Any, List

from popoll_backend.model import Payload


class Instrument(Payload):
    
    def __init__(self, data: List[Any]):
        self.id: int = data[0]
        self.name: str = data[1]

    @classmethod
    def create_table(cls):
        return """CREATE TABLE IF NOT EXISTS instruments (
            id integer PRIMARY KEY,
            name text NOT NULL
        );"""