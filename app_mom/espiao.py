import random
import time
from pprint import pprint

import Pyro4

from app.objects import TupleObject
from config import PYRO_BROKER_PORT, PYRO_BROKER_HOST, PYRO_BROKER_NAME, PYRO_CHAT_NAME, PYRO_CHAT_HOST, PYRO_CHAT_PORT


class Espiao:
    broker = None
    logger = None

    name = None
    topic_name = None
    value = None

    monitor = None
    min_target = None
    max_target = None

    calls = 0
    random = None
    timer = None
    active = None
    monitor_types = ["Temperatura", "Umidade", "Velocidade"]
    buffer = None
    counter = None

    def __init__(self, name=None, topic_name=None, monitor=None):
        if name is None:
            name = f"sensor_{random.randint(1000,9999)}"

        if topic_name is None:
            topic_name = f"topic_{random.randint(1000,9999)}"

        if monitor is None or monitor > len(self.monitor_types):
            monitor = random.randint(1, 3)

        self.min_target = 0
        self.max_target = 10
        self.monitor = monitor - 1
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
        self.monitor_msgs.append(msg)

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
        self.insert_message(f"[ENCONTRADA] {msg.message}")


    def update(self):
        now = time.time()
        if now - self.counter < 0.16:
            return

        msgs_on_server = self.chat_server.scan(
            TupleObject().pickled()
        )

        for msg in msgs_on_server:
            msg = TupleObject.pickle_deserialize(msg)
            for msg_contains in self.monitor_msgs:
                if msg_contains in msg.message:
                    self.add_message_to_broker(msg)
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
