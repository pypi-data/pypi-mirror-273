import sqlite3

from popoll_backend.model import Payload
from popoll_backend.query import Query
from popoll_backend.query.get_poll import GetPoll


class UpdatePoll(Query):
    
    name: str
    color: str
    
    def __init__(self, poll: str, name: str, color: str):
        super().__init__(poll)
        self.name = name
        self.color = color
        
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('UPDATE options SET name=?, color=?', (self.name, self.color))
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return GetPoll(self.poll).run(cursor)