import contextlib
import datetime
import flask
import json
import jsonpickle

from popoll_backend.model import Payload

class History(Payload):
    
    def __init__(self, request: flask.Request, response, kwargs):
        self.date = datetime.datetime.now().isoformat(sep='T', timespec='auto')
        self.method = request.method
        self.path = request.path
        self.matching_path = request.url_rule.rule
        self.ip = request.headers.get('Host', None)
        self.sessionId = request.headers.get('SessionId', None)
        self.queryParams = kwargs
        self.body = request.data
        with contextlib.suppress(Exception):
            self.body_json = json.loads(request.data)
        self.response = response