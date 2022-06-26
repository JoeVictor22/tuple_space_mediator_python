from config import PYRO_BROKER_NAME, PYRO_BROKER_HOST, PYRO_BROKER_PORT

if __name__ == "__main__":
    import Pyro4

    with Pyro4.Proxy(
        f"PYRO:{PYRO_BROKER_NAME}@{PYRO_BROKER_HOST}:{PYRO_BROKER_PORT}"
    ) as p:
        try:
            p._pyroBind()

            choice = input(
                "Digite: \n1 (para criar um mediador)\n2 (para criar um espião)\n"
            )

            if choice == "1":
                from app_mom.Mediador import Mediador

                print("Criando Mediador")
                cliente = Mediador()
                from app_mom.mediador_interface import start

                start(cliente)

            elif choice == "2":
                from app_mom.espiao import Espiao

                print("Criando Espião")
                topic = input("Digite o tópico (vazio para gerar aleatorio)\n")

                sensor = Espiao(topic_name=topic)
                from app_mom.espiao_interface import start

                start(sensor)

            else:
                print("Opção invalida")

        except Pyro4.errors.CommunicationError as eee:
            from app_mom.server import start_server

            print(eee)

            print("Iniciando servidor")
            start_server()
