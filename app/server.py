from copy import deepcopy
import uuid

import Pyro4
from pprint import pprint
from app.objects import TupleObject
from typing import List


@Pyro4.expose
class Servidor(object):
    tuple_space: List[TupleObject] = list()

    def _search_for_tuples(self, tupla):
        yield from filter(lambda obj: tupla.is_equal_to(obj), self.tuple_space)

    def write(self, tupla):
        tupla = TupleObject.pickle_deserialize(tupla)
        if not isinstance(tupla, TupleObject):
            return

        tupla.uuid = uuid.uuid4()
        self.tuple_space.append(tupla)

        pprint(f"[write]: {tupla}")

    def take(self, tupla):
        tupla = TupleObject.pickle_deserialize(tupla)
        if not isinstance(tupla, TupleObject):
            return

        next_tuple = next(self._search_for_tuples(tupla))
        tuple_found = deepcopy(next_tuple)
        self.tuple_space.remove(next_tuple)

        pprint(f"[take]: {tupla} - {next_tuple}")

        return TupleObject.pickle_serialize(tuple_found)

    def read(self, tupla):
        tupla = TupleObject.pickle_deserialize(tupla)
        if not isinstance(tupla, TupleObject):
            return

        next_tuple = next(self._search_for_tuples(tupla))

        pprint(f"[read]: {tupla} - {next_tuple}")

        return TupleObject.pickle_serialize(next_tuple)

    def scan(self, tupla):
        tupla = TupleObject.pickle_deserialize(tupla)
        if not isinstance(tupla, TupleObject):
            return

        tuples = list(self._search_for_tuples(tupla))

        pprint(f"[scan]: {tupla} - {tuples}")

        return [TupleObject.pickle_serialize(obj) for obj in tuples]

    def count(self, tupla):
        tupla = TupleObject.pickle_deserialize(tupla)
        if not isinstance(tupla, TupleObject):
            return

        tuples = list(self._search_for_tuples(tupla))

        pprint(f"[count]: {tupla} - {len(tuples)}")

        return len(tuples)


def start_server():
    Pyro4.Daemon.serveSimple(
        {
            Servidor: "Tuplas",
        },
        host="0.0.0.0",
        port=9090,
        verbose=True,
        ns=False,
    )
    pprint(f"[starting server]")
