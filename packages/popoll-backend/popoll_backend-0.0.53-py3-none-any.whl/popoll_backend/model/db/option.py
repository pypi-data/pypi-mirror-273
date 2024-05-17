from typing import Any, List

from popoll_backend.model import Payload


class Option(Payload):
    
    def __init__(self, data: List[Any]):
        self.name: str = data[0]
        self.color: str = data[1]

    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS options (
            name text,
            color text 
        ); """