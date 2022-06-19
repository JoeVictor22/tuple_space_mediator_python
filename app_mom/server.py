from queue import Queue
from typing import List

import Pyro4


@Pyro4.expose
class Servidor(object):
    topics = {}

    def _get_topic(self, topic_name) -> Queue:
        return self.topics.get(topic_name, None)

    def get_topics(self) -> List[str]:
        return [key for key in self.topics]

    def create_topic(self, topic_name) -> bool:
        if topic_name in self.topics:
            # already exists
            return False

        self.topics[topic_name] = Queue()
        print(f"[New topic] {topic_name}")
        return True

    def publish(self, topic_name, message, formated_msg) -> bool:
        queue = self._get_topic(topic_name)

        if not queue:
            self.create_topic(topic_name)

        queue = self._get_topic(topic_name)
        queue.put(formated_msg)
        print(f"[Published] {formated_msg}")

        return True

    def subscribe(self, topic_name) -> str:
        queue = self._get_topic(topic_name)

        if not queue:
            self.create_topic(topic_name)
            return ""

        if queue.empty():
            return ""

        message = queue.get()
        print(f"[Subscribe] [{topic_name}] - {message}")

        return message


def start_server():
    Pyro4.Daemon.serveSimple(
        {
            Servidor: "Broker",
        },
        host="0.0.0.0",
        port=9090,
        ns=False,
        verbose=True,
    )
    print(f"[Server started]")
