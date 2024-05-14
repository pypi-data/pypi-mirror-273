
from typing import List
from popoll_backend.model import Payload
from popoll_backend.model.payload.user import UserOut


class UsersPayloadDetails(Payload):
    
    def __init__(self, users: List[UserOut]):
        self.users: List[UserOut] = users