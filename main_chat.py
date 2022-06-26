import Pyro4

from config import PYRO_CHAT_NAME, PYRO_CHAT_HOST, PYRO_CHAT_PORT


if __name__ == "__main__":

    with Pyro4.Proxy(f"PYRO:{PYRO_CHAT_NAME}@{PYRO_CHAT_HOST}:{PYRO_CHAT_PORT}") as p:
        try:
            p._pyroBind()

            from app.client import Client

            print("[system] Criando Cliente")
            name = input("Digite o seu nome\n")

            if name == "":
                name = "joao"

            from app.chat_interface import Interface

            a = Interface(name=name).start()

        except Pyro4.errors.CommunicationError as eee:
            from app.server import start_server

            print(eee)

            print("[system] Criando servidor")
            start_server()
