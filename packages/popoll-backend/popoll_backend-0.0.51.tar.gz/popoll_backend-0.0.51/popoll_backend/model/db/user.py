from typing import Any, List

from popoll_backend.model import Payload


class User(Payload):
    
    def __init__(self, data: List[Any]):
        self.id: int = data[0]
        self.name: str = data[1]

    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL UNIQUE
        ); """