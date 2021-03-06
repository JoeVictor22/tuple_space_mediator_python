import base64
import pickle
from dataclasses import dataclass
from uuid import uuid1 as UUID


@dataclass
class TupleObject:
    uuid: UUID = None
    dest: str = None
    who: str = None
    chat_room: str = None
    message: str = None
    tipo: str = "spy"

    @staticmethod
    def pickle_deserialize(obj):
        obj = base64.b64decode(obj["data"])
        return pickle.loads(obj)

    @staticmethod
    def pickle_serialize(obj):
        return pickle.dumps(obj)

    def pickled(self):
        return TupleObject.pickle_serialize(self)

    def is_equal_to(self, tupla):
        # TODO add new key tipo
        keys = ["chat_room", "dest", "who", "tipo"]

        for key in keys:
            if (
                getattr(self, key)
                and getattr(tupla, key)
                and getattr(self, key) != getattr(tupla, key)
            ):
                return False
        return True
