from typing import Any, List

from popoll_backend.model import Payload

class Answer(Payload):
    
    def __init__(self, data: List[Any]):
        self.id: int = data[0]
        self.user_id: int = data[1]
        self.date_id: int = data[2]
        self.response: bool = bool(data[3])

    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS answers (
            id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            date_id integer NOT NULL REFERENCES dates(id) ON DELETE CASCADE,
            response boolean NOT NULL,
            UNIQUE(user_id, date_id)
        ); """