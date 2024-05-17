import json
import jsonpickle

from typing import Any, List

class Payload:
    
    def toJSON(self):
        return json.loads(jsonpickle.encode(self, unpicklable=False))
    
    def toDict(self, llist: List[Any]):
        return {i.id: i for i in llist}