from typing import Any, List

from popoll_backend.model import Payload


class Session(Payload):
    
    def __init__(self, data: List[Any]):
        self.id: int = data[0]
        self.session_id: str = data[1]
        self.user_id: int = data[2]

    @classmethod
    def create_table(cls):
        return """CREATE TABLE IF NOT EXISTS sessions (
            id integer PRIMARY KEY,
            session_id text NOT NULL,
            user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            datetime text NOT NULL
        );"""