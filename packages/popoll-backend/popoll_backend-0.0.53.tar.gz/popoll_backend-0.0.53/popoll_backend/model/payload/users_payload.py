
from typing import List
from popoll_backend.model.db.user import User
from popoll_backend.model import Payload


class UsersPayload(Payload):
    
    def __init__(self, users: List[User]):
        self.users: List[User] = users