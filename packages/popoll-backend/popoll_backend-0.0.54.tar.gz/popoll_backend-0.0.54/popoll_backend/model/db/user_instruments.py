from typing import Any, List

from popoll_backend.model import Payload


class UserInstruments(Payload):
    
    def __init__(self, data: List[Any]):
        self.id: int = data[0]
        self.user_id: int = data[1]
        self.instrument_id: int = data[2]
        self.is_main: bool = bool(data[3])

    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS user_instruments (
            id integer PRIMARY KEY,
            user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            instrument_id integer,
            is_main boolean NOT NULL
        ); """