import random
import time

import Pyro4

from config import PYRO_BROKER_PORT, PYRO_BROKER_HOST, PYRO_BROKER_NAME


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
        self.random = False
        self.timer = 1
        self.calls = 0
        self.active = False
        self.buffer = list()
        self.counter = time.time()

    def add_new_msg(self, msg):
        print(f"NOVA MSG:  {msg}")

    def update(self):
        now = time.time()
        if now - self.counter < 0.16:
            return

        # TODO, get messages from chat
        # self.broker.publish(self.topic_name, self.value, message)
        # self.insert_message(message)

        rand = random.randint(0, 10)
        if rand == 3:
            print("ACHOU MSG")

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
