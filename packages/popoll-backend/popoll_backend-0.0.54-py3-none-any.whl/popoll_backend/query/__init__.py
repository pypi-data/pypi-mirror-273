import flask
import os
import sqlite3

from typing import Type

from popoll_backend.model import Payload


class Query:
    
    fail_if_db_exists: bool = False
    fail_if_db_not_exists: bool = True
    
    def __init__(self, poll: str):
        self.poll = poll
        self.db_file = f'{poll}.db'
        if self.fail_if_db_exists and os.path.exists(self.db_file):
            flask.abort(409, f'The poll [{poll}] already exists.')
        if self.fail_if_db_not_exists and not os.path.exists(self.db_file):
            flask.abort(400, f'The poll [{poll}] does not exist.')
    
    def run(self, cursor: sqlite3.Cursor=None):
        if cursor:
            return self._run(cursor)
        else:
            with sqlite3.connect(self.db_file) as connection:
                cursor: sqlite3.Cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute("ATTACH DATABASE 'instruments.db' AS instruments;")
                return self._run(cursor).toJSON()
            
    def _run(self, cursor: sqlite3.Cursor):
        try:
            self.process(cursor)
            return self.buildResponse(cursor)
        except sqlite3.Error as e:
            print(e)
            self.error(e)
            if e.sqlite_errorcode == sqlite3.SQLITE_ERROR:
                flask.abort(500, 'Main error. Are you sure database exists?')
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        raise NotImplementedError()
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        raise NotImplementedError()
    
    def error(self, e: sqlite3.Error):
        pass
    
    def selectItem(self, cursor: sqlite3.Cursor, query: str, id: int, type: Type[Payload]) -> Payload:
        res = cursor.execute(query, (id,)).fetchall()
        if len(res) == 0:
            flask.abort(404, f'Object of type [{type.__name__}] and id [{id}] has not been found.')
        if len(res) > 1:
            print('\n\t'.join([
                'More than 1 result for following query. This is not expected.',
                f'query={query}',
                f'id={id}',
                f'res={res}'
            ]))
        return type(res[-1])