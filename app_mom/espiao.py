import random
import time
from pprint import pprint

import Pyro4

from app.objects import TupleObject
from config import (
    PYRO_BROKER_PORT,
    PYRO_BROKER_HOST,
    PYRO_BROKER_NAME,
    PYRO_CHAT_NAME,
    PYRO_CHAT_HOST,
    PYRO_CHAT_PORT,
)


class Espiao:
    broker = None
    logger = None

    name = None
    topic_name = None
    value = None

    min_target = None
    max_target = None

    calls = 0
    random = None
    timer = None
    active = None
    buffer = None
    counter = None

    def __init__(self, name=None, topic_name=None):
        if name is None:
            name = f"sensor_{random.randint(1000,9999)}"

        if topic_name is None:
            topic_name = f"topic_{random.randint(1000,9999)}"

        self.min_target = 0
        self.max_target = 10
        self.name = name
        self.value = 0
        self.topic_name = topic_name
        self.broker = Pyro4.core.Proxy(
            f"PYRO:{PYRO_BROKER_NAME}@{PYRO_BROKER_HOST}:{PYRO_BROKER_PORT}"
        )
        self.chat_server = Pyro4.core.Proxy(
            f"PYRO:{PYRO_CHAT_NAME}@{PYRO_CHAT_HOST}:{PYRO_CHAT_PORT}"
        )
        self.random = False
        self.timer = 1
        self.calls = 0
        self.active = False
        self.buffer = list()
        self.counter = time.time()
        self.monitor_msgs = list()
        self.messages_id = list()
        self.messages = list()

    def add_new_msg(self, msg):
        if msg not in self.monitor_msgs:
            # self.send_message(msg)
            self.monitor_msgs.append(msg)

    def send_message(self, message, dest=None, room=None):
        new_tuple = TupleObject(
            who=self.name, message=message, dest=dest, chat_room=room, tipo="spy"
        )
        self._send_to_server(new_tuple)

    def _send_to_server(self, tuple):
        self.broker.write(tuple.pickled())

    def add_messages_to_buffer(self, messages):
        msgs = map(TupleObject.pickle_deserialize, messages)
        added_msgs = [
            self._add_new_message(msg)
            for msg in msgs
            if not self._exists_in_client(msg)
        ]

    def _exists_in_client(self, message):
        if message.uuid in self.messages_id:
            return True
        return False

    def _add_new_message(self, message):
        if not message.uuid:
            return
        return message

    def add_message_to_broker(self, msg):
        pprint(msg)
        if self._exists_in_client(msg):
            return

        self.messages.append(msg)
        self.messages_id.append(msg.uuid)
        self.broker.publish(self.topic_name, self.value, msg.message)
        self.insert_message(f"[BLOQUEADA] {msg.message}")

    def add_message_allowed(self, msg):
        pprint(msg)
        if self._exists_in_client(msg):
            return

        self.messages.append(msg)
        self.messages_id.append(msg.uuid)
        self.insert_message(f"[VERIFICADA] {msg.message}")
        msg.tipo = "chat"
        self.chat_server.write(msg.pickled())

    def update(self):
        now = time.time()
        if now - self.counter < 0.16:
            return

        msgs_on_server = self.chat_server.scan(TupleObject().pickled())

        for msg in msgs_on_server:
            msg = TupleObject.pickle_deserialize(msg)
            blocked = False
            for msg_contains in self.monitor_msgs:
                if msg_contains in msg.message:
                    self.add_message_to_broker(msg)
                    blocked = True
            if not blocked:
                self.add_message_allowed(msg)

        self.counter = time.time()

    def insert_message(self, message):
        message = self.format_message(str(message))
        self.buffer.append(message)

    @staticmethod
    def format_message(message):
        import time

        # from datetime import datetime
        # time = datetime.now().strftime("%H:%M:%S")
        time = time.time()
        return f"[{time}] - {message}"
