import random
from datetime import datetime
from pprint import pprint
import uuid

import Pyro4

from config import PYRO_URL

import time

from app.objects import TupleObject


class Client:
    server = None

    name = None

    buffer = []
    rooms = set()
    messages = []

    room = None

    counter = None

    messages_id = []

    def __init__(self, room="default", name=None):
        self.name = name
        self.room = room
        self.server = Pyro4.core.Proxy(PYRO_URL)
        self.counter = time.time()

    def update(self):
        now = time.time()
        if now - self.counter < 3:
            return

        if self.room:
            msgs_on_server = self.server.scan(
                TupleObject(chat_room=self.room).pickled()
            )
            # private_msgs = self.server.scan(
            #     TupleObject(chat_room=self.room, dest=self.name).pickled()
            # )

            # global_msgs = self.server.scan(TupleObject().pickled())
            self.add_global_messages_to_buffer(msgs_on_server)
            # self.add_messages_to_buffer(private_msgs)
            # msgs = map(TupleObject.pickle_deserialize, msgs_on_server)
            # pprint(list(msgs))

            # self.add_messages_to_buffer(global_msgs)

    def get_participants(self):
        if not self.room:
            return []

        people = set()
        msgs = self.server.scan(TupleObject(chat_room=self.room).pickled())

        for msg in msgs:
            msg = TupleObject.pickle_deserialize(msg)
            if msg.who:
                people.add(msg.who)

        return people

    def get_participants_from_room(self, room):

        people = set()
        msgs = self.server.scan(TupleObject(chat_room=room).pickled())

        for msg in msgs:
            msg = TupleObject.pickle_deserialize(msg)
            people.add(msg.who)

        return people

    def get_rooms(self):
        rooms = set()
        msgs = self.server.scan(TupleObject().pickled())

        for msg in msgs:
            msg = TupleObject.pickle_deserialize(msg)
            rooms.add(msg.chat_room)

        return rooms

    def change_room(self, room):
        # if self.name in self.get_participants_from_room(room):
        #     msg = TupleObject(
        #         message=f"[sistema] Já existe um usuário com o nome {self.name} nesta sala"
        #     )
        #     msg.uuid = uuid.uuid4()
        #     self._add_new_message(msg)
        #     return False

        if room in self.get_rooms():
            self.room = room
            self.send_message(message=f"{self.name} entrou na sala", room=room)
            return True
        return False

    def send_message(self, message, dest=None, room=None):
        new_tuple = TupleObject(
            who=self.name, message=message, dest=dest, chat_room=room
        )
        self._send_to_server(new_tuple)

    def create_room(self, room):
        new_tuple = TupleObject(message="Criando nova sala", chat_room=room)
        self._send_to_server(new_tuple)

    def _send_to_server(self, tuple):
        self.server.write(tuple.pickled())

    def _exists_in_client(self, message):
        if message.uuid in self.messages_id:
            return True
        return False

    def _add_new_message(self, message):
        if not message.uuid:
            return

        self.messages.append(message)
        self.messages_id.append(message.uuid)

        return message

    def _add_new_global_message(self, message):
        if not message.uuid:
            return

        if message.dest and message.dest != self.name and message.who != self.name:
            return

        self.messages.append(message)
        self.messages_id.append(message.uuid)

        return message

    def add_messages_to_buffer(self, messages):
        msgs = map(TupleObject.pickle_deserialize, messages)
        added_msgs = [
            self._add_new_message(msg)
            for msg in msgs
            if not self._exists_in_client(msg)
        ]

    def add_global_messages_to_buffer(self, messages):
        msgs = map(TupleObject.pickle_deserialize, messages)
        added_msgs = [
            self._add_new_global_message(msg)
            for msg in msgs
            if not self._exists_in_client(msg)
        ]
