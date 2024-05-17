#! /usr/bin/python3
import argparse
import sys
import flask
import json
import logging
import logging.handlers
import os

from flask_cors import CORS
from flask_restful import Api, Resource
from functools import wraps
from typing import Any, Dict

from popoll_backend.model.payload.history import History
from popoll_backend.query.create_answer import CreateAnswer
from popoll_backend.query.create_date import CreateDate
from popoll_backend.query.create_instrument import CreateInstrument
from popoll_backend.query.create_poll import CreatePoll
from popoll_backend.query.create_user import CreateUser
from popoll_backend.query.delete_answer import DeleteAnswer
from popoll_backend.query.delete_date import DeleteDate
from popoll_backend.query.delete_user import DeleteUser
from popoll_backend.query.get_date import GetDate
from popoll_backend.query.get_dates import GetDates
from popoll_backend.query.get_instruments import GetInstruments
from popoll_backend.query.get_poll import GetPoll
from popoll_backend.query.get_search_answer import GetSearchAnswer
from popoll_backend.query.get_session import GetSession
from popoll_backend.query.get_user import GetUser
from popoll_backend.query.get_users import GetUsers
from popoll_backend.query.update_answer import UpdateAnswer
from popoll_backend.query.update_date import UpdateDate
from popoll_backend.query.update_poll import UpdatePoll
from popoll_backend.query.create_session import CreateSession
from popoll_backend.query.update_user import UpdateUser


app = flask.Flask(__name__)
CORS(app)
api = Api(app)


def body(request: flask.request, param: str, default: Any=None, mandatory=True):
    _body = json.loads(request.data)
    return _body[param] if mandatory else _body.get(param, default)



def history(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        res = f(*args, **kwargs)
        os.makedirs(os.path.join('.history', kwargs["poll"]), exist_ok=True)
        logger = logging.getLogger('my_logger')
        logger.handlers.clear()
        handler = logging.handlers.RotatingFileHandler(os.path.join('.history', kwargs["poll"], f'{kwargs["poll"]}.history.log'), maxBytes=1024*1024, backupCount=10)
        logger.addHandler(handler)
        logger.warning(json.dumps(History(flask.request, res, kwargs).toJSON()))
        return res
    return decorated


class PollEndpoint(Resource):
    def get(self, poll: str): return GetPoll(poll).run()
    
    @history
    def post(self, poll:str): return CreatePoll(poll, body(flask.request, 'name', mandatory=False, default=poll), body(flask.request, 'instruments', mandatory=False, default=[]), body(flask.request, 'color', mandatory=False, default="#000000")).run()
    
    @history
    def put(self, poll:str): return UpdatePoll(poll, body(flask.request, 'name'), body(flask.request, 'color')).run()
    
    
    

class InstrumentsEndpoint(Resource):
    def get(self, poll: str) -> Dict[str, Any]: return GetInstruments(poll).run()
    
    @history
    def post(self, poll: str) -> int: return CreateInstrument(poll, body(flask.request, 'name')).run()







class UsersEndpoint(Resource):
    def get(self, poll: str) -> Dict[str, Any]: return GetUsers(poll, details=True).run()
    
    @history
    def post(self, poll: str) -> int: return CreateUser(poll, body(flask.request, 'user')['name'], body(flask.request, 'main_instrument')['id'], [i['id'] for i in body(flask.request, 'instruments')]).run()



class UserEndpoint(Resource):
    def get(self, poll: str, id:int) -> Dict[str, Any]: return GetUser(poll, id, details=True).run()
    
    @history
    def put(self, poll: str, id: int) -> int: return UpdateUser(poll, id, body(flask.request, 'user')['name'], body(flask.request, 'main_instrument')['id'], [i['id'] for i in body(flask.request, 'instruments')]).run()
    
    @history
    def delete(self, poll: str, id: int) -> int: return DeleteUser(poll, id).run()







class DatesEndpoint(Resource):
    def get(self, poll: str): return GetDates(poll).run()
    
    @history
    def post(self, poll: str) -> int: return CreateDate(poll, body(flask.request, 'title'), body(flask.request, 'date'), body(flask.request, 'time', mandatory=False), body(flask.request, 'end_time', mandatory=False)).run()



class DateEndpoint(Resource):
    def get(self, poll: str, id:int) -> Dict[str, Any]: return GetDate(poll, id, details=True).run()
    
    @history
    def put(self, poll: str, id: int) -> int: return UpdateDate(poll, id, body(flask.request, 'title'), body(flask.request, 'date'), body(flask.request, 'time', mandatory=False), body(flask.request, 'end_time', mandatory=False)).run()
    
    @history
    def delete(self, poll: str, id: int) -> int: return DeleteDate(poll, id).run()







class AnswersEndpoint(Resource):
    
    @history
    def post(self, poll: str) -> int: return CreateAnswer(poll, body(flask.request, 'user_id'), body(flask.request, 'date_id')).run()


class AnswerEndpoint(Resource):
    
    @history
    def put(self, poll: str, id: int) -> int: return UpdateAnswer(poll, id, body(flask.request, 'response')).run()
    
    @history
    def delete(self, poll: str, id: int) -> int: return DeleteAnswer(poll, id).run()

class GetAnswerEndpoint(Resource):
    def get(self, poll: str, userId: int, dateId: int): return GetSearchAnswer(poll, userId, dateId).run()


class SessionEndpoint(Resource):
    def get(self, poll: str, id: str): return GetSession(poll, id).run()
    
    @history
    def post(self, poll: str, id: str): return CreateSession(poll, id, body(flask.request, 'user_id')).run()



class GlobalInstrumentsEndpoint(Resource):
    def get(self): return GetInstruments('__global').run()
    
    @history
    def post(self) -> int: return CreateInstrument('__global', body(flask.request, 'name')).run()


api.add_resource(GlobalInstrumentsEndpoint, '/instrument')

api.add_resource(PollEndpoint, '/<string:poll>')
api.add_resource(InstrumentsEndpoint, '/<string:poll>/instrument')
api.add_resource(UsersEndpoint, '/<string:poll>/user')
api.add_resource(UserEndpoint, '/<string:poll>/user/<int:id>')
api.add_resource(DatesEndpoint, '/<string:poll>/date')
api.add_resource(DateEndpoint, '/<string:poll>/date/<int:id>')
api.add_resource(AnswersEndpoint, '/<string:poll>/answer')
api.add_resource(AnswerEndpoint, '/<string:poll>/answer/<int:id>')
api.add_resource(GetAnswerEndpoint, '/<string:poll>/answer/<int:userId>/<int:dateId>')
api.add_resource(SessionEndpoint, '/<string:poll>/session/<string:id>')

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='the hostname to listen on', default='0.0.0.0')
    parser.add_argument('--port', help='the port of the webserver', default=4444)
    parser.add_argument('--debug', help='Enable debugging', action='store_true')
    return parser

def run(args):
    app.run(debug=args.debug, host=args.host, port=args.port)

if __name__ == '__main__':
    args = get_options().parse_args()
    run(args)
