import tkinter as tk
from tkinter import ttk

import Pyro4

from app.client import Client
from config import PYRO_URL


class Interface:
    master = tk.Tk()
    # master.geometry('200x150')

    form = {}
    checkbox = {}
    input = {
        "input": {
            "value": tk.StringVar(),
            "message": "Digita algo ai",
            "label": None,
            "button": None,
            "input": None,
        },
        "chat": {
            "value": tk.StringVar(),
            "message": "Este é o chat",
            "label": None,
            "button": None,
            "input": None,
        },
        "select": {
            "value": tk.StringVar(),
            "message": "Selecione a sala",
            "label": None,
            "button": None,
            "input": None,
        },
        "select_room": {
            "value": tk.StringVar(),
            "message": "Selecione a sala",
            "label": None,
            "button": None,
            "input": None,
        },
        "select_people": {
            "value": tk.StringVar(),
            "message": "Lista de participantes",
            "label": None,
            "button": None,
            "input": None,
        },
        "people": {
            "value": tk.StringVar(),
            "message": "Participantes",
            "label": None,
            "button": None,
            "input": None,
        },
        "create_room": {
            "value": tk.StringVar(),
            "message": "Criar sala",
            "label": None,
            "button": None,
            "input": None,
        },
        "private_msg": {
            "value": tk.StringVar(),
            "message": "Selecionar participante",
            "label": None,
            "button": None,
            "input": None,
        },
        "private_msg_txt": {
            "value": tk.StringVar(),
            "message": "Mensagem",
            "label": None,
            "button": None,
            "input": None,
        },
    }
    popup_room = None
    popup_people = None

    logged_room = tk.StringVar()

    OPTIONS_ROW = 5
    TEXT_COL = 10
    topics = []
    choose = []
    buffer = []
    buffer_len = 50
    broker = Pyro4.core.Proxy(PYRO_URL)
    label_test = None

    row = 0

    text_width = 50
    chatrooms = []
    people = []
    private = None  # private target

    client = None  # client object

    def __init__(self, name):
        self.client = Client(name=name)

    def create_message(self, messages):
        final_txt = ""

        for message in messages:
            final_txt += f"{message}\n"
        return final_txt

    def send_message(self):
        input_value = self.input["input"]["input"].get()
        print(f"enviando: {input_value} - {self.get_room()}")
        if self.private:
            self.client.send_message(
                input_value, room=self.get_room(), dest=self.private
            )
        else:
            self.client.send_message(input_value, room=self.get_room())

    def get_room(self):
        return self.input["select"]["value"].get()

    def update_chat_text(self, value):
        self.input["chat"]["input"].delete(1.0, "end")
        self.input["chat"]["input"].insert("end", value)

    def create_input(self):
        # input
        self.input["input"]["input"] = tk.Entry(self.master, width=self.text_width)
        self.input["input"]["input"].grid(row=self.row, column=0, columnspan=2)
        # button
        self.input["input"]["button"] = tk.Button(
            self.master, text="Enviar", command=self.send_message, bd=3
        )
        self.input["input"]["button"].grid(row=self.row, column=2, columnspan=1)
        self.row += 1

    def create_chat(self):
        # label
        room_label = tk.Label(self.master, text="SALA ATUAL: ")
        room_label.config(font=("helvetica", 10))
        room_label.grid(row=self.row, column=0, columnspan=1)

        room_label = tk.Label(self.master, textvariable=self.input["select"]["value"])
        room_label.config(font=("helvetica", 10))
        room_label.grid(row=self.row, column=1, columnspan=2)

        # chat
        self.row += 1
        self.input["chat"]["input"] = tk.Text(
            self.master, state="normal", width=self.text_width
        )
        scrollbar = tk.Scrollbar(self.input["chat"]["input"])
        scrollbar.place(relheight=1, relx=0.974)

        self.input["chat"]["input"].grid(row=self.row, column=0, columnspan=3)
        self.row += 1

    def create_dropdown(self):
        # label
        self.input["select_room"]["label"] = tk.Label(
            self.master, text=self.input["select_room"]["message"]
        )
        self.input["select_room"]["label"].config(font=("helvetica", 10))
        self.input["select_room"]["label"].grid(row=self.row, column=0, columnspan=1)

        # select
        self.input["select_room"]["value"].set("nenhuma")
        self.input["select_room"]["input"] = tk.OptionMenu(
            self.master, self.input["select_room"]["value"], "nenhuma", *self.chatrooms
        )
        self.input["select_room"]["input"].grid(row=self.row, column=1, columnspan=1)

        # button
        self.input["select_room"]["button"] = tk.Button(
            self.master, text="Atualizar lista", command=self.update_chatrooms, bd=3
        )
        self.input["select_room"]["button"].grid(row=self.row, column=2, columnspan=1)
        self.row += 1

        # select participante
        # label
        self.input["select_people"]["label"] = tk.Label(
            self.master, text=self.input["select_people"]["message"]
        )
        self.input["select_people"]["label"].config(font=("helvetica", 10))
        self.input["select_people"]["label"].grid(row=self.row, column=0, columnspan=1)

        self.input["select_people"]["value"].set("nenhuma")
        self.input["select_people"]["input"] = tk.OptionMenu(
            self.master,
            self.input["select_people"]["value"],
            "nenhuma",
            *self.people,
        )
        self.input["select_people"]["input"].grid(row=self.row, column=1, columnspan=1)

        # button
        self.input["select_people"]["button"] = tk.Button(
            self.master,
            text="Atualizar participantes",
            command=self.update_people,
            bd=3,
        )
        self.input["select_people"]["button"].grid(row=self.row, column=2, columnspan=1)
        self.row += 1

        self.input["create_room"]["button"] = tk.Button(
            self.master, text="Criar nova sala", command=self.create_room_popoup, bd=3
        )
        self.input["create_room"]["button"].grid(row=self.row, column=2, columnspan=1)
        self.row += 1

        self.input["private_msg"]["button"] = tk.Button(
            self.master, text="Enviar msg privada", command=self.private_msg_popup, bd=3
        )
        self.input["private_msg"]["button"].grid(row=self.row, column=2, columnspan=1)
        self.row += 1

    def private_msg_popup(self):

        if self.popup_people:
            return

        self.popup_people = tk.Toplevel()
        self.popup_people.wm_title("Window")

        self.input["private_msg"]["label"] = tk.Label(
            self.popup_people, text=self.input["private_msg"]["message"]
        )
        self.input["private_msg"]["label"].config(font=("helvetica", 10))
        self.input["private_msg"]["label"].grid(row=0, column=0, columnspan=2)

        # select participante
        self.input["private_msg"]["value"].set("nenhuma")
        self.input["private_msg"]["input"] = tk.OptionMenu(
            self.popup_people,
            self.input["private_msg"]["value"],
            "nenhuma",
            *self.client.get_participants(),
        )
        self.input["private_msg"]["input"].grid(row=1, column=0, columnspan=2)

        self.input["private_msg_txt"]["label"] = tk.Label(
            self.popup_people, text=self.input["private_msg_txt"]["message"]
        )
        self.input["private_msg_txt"]["label"].config(font=("helvetica", 10))
        self.input["private_msg_txt"]["label"].grid(row=2, column=0, columnspan=2)

        # input
        self.input["private_msg_txt"]["input"] = tk.Entry(
            self.popup_people, width=self.text_width
        )
        self.input["private_msg_txt"]["input"].grid(row=3, column=0, columnspan=2)

        b = ttk.Button(
            self.popup_people, text="Enviar", command=self.send_private_message
        )
        b.grid(row=4, column=0)

    def send_private_message(self):
        destino = self.input["private_msg"]["value"].get()
        msg = self.input["private_msg_txt"]["input"].get()
        self.private = None

        print(f"destino:{destino} - msg:{msg}")

        self.client.send_message(msg, room=self.get_room(), dest=destino)

        self.popup_people.destroy()
        self.popup_people = None

    def create_room_popoup(self):

        if self.popup_room:
            return

        self.popup_room = tk.Toplevel()
        self.popup_room.wm_title("Window")

        self.input["create_room"]["label"] = tk.Label(
            self.popup_room, text=self.input["create_room"]["message"]
        )
        self.input["create_room"]["label"].config(font=("helvetica", 10))
        self.input["create_room"]["label"].grid(row=0, column=0, columnspan=2)

        # input
        self.input["create_room"]["input"] = tk.Entry(
            self.popup_room, width=self.text_width
        )
        self.input["create_room"]["input"].grid(row=1, column=0, columnspan=3)

        b = ttk.Button(self.popup_room, text="Criar", command=self.create_room)
        b.grid(row=2, column=0)

    def update_people(self):
        self.people = list(self.client.get_participants())

        sala = self.input["select_people"]["value"].get()

        menu = self.input["select_people"]["input"]["menu"]
        variable = self.input["select_people"]["value"]
        menu.delete(0, "end")
        variable.set("nenhuma")

        menu.add_command(
            label="nenhuma", command=lambda value="nenhuma": variable.set(value)
        )

        for string in self.people:
            menu.add_command(
                label=string, command=lambda value=string: variable.set(value)
            )

    def update_chatrooms(self):

        self.chatrooms = list(self.client.get_rooms())

        sala = self.input["select_room"]["value"].get()

        if sala in self.chatrooms and self.client.change_room(sala):
            self.input["select"]["value"].set(sala)

        menu = self.input["select_room"]["input"]["menu"]
        variable = self.input["select_room"]["value"]
        menu.delete(0, "end")
        variable.set("nenhuma")

        menu.add_command(
            label="nenhuma", command=lambda value="nenhuma": variable.set(value)
        )

        for string in self.chatrooms:
            menu.add_command(
                label=string, command=lambda value=string: variable.set(value)
            )

    def create_room(self):
        print(f"criadno nova sala {self.input['create_room']['input'].get()}")
        room = self.input["create_room"]["input"].get()
        self.client.create_room(room)
        self.popup_room.destroy()
        self.popup_room = None

    def start(self):
        self.create_input()
        # self.create_people()
        self.create_dropdown()
        self.create_chat()

        # do loop here

        while True:
            self.master.update()
            self.client.update()

            txt = "\n".join([self.create_msg(msg) for msg in self.client.messages])
            self.update_chat_text(txt)

    def create_msg(self, message):
        txt = ""
        if message.dest:
            txt += f"[PRIVATE] [to/{message.dest}] "

        if message.chat_room:
            txt += f"[room/{message.chat_room}] "

        if message.who:
            txt += f"[from/{message.who}] "

        txt += f"{message.message}"

        return txt

    def select_choice(self):
        pass

    def create_people(self):
        self.input["people"]["label"] = tk.Label(
            self.master, text=self.input["people"]["message"]
        )
        self.input["people"]["label"].config(font=("helvetica", 10))
        self.input["people"]["label"].grid(row=self.row, column=0, columnspan=1)
        self.row += 1

        choose = []
        col = 0

        for value in self.client.get_participants():
            var = tk.BooleanVar()
            choose.append(var)
            c = tk.Checkbutton(
                self.master,
                text=value,
                variable=var,
                onvalue=1,
                offvalue=0,
                command=self.select_choice,
            )

            if col == 3:
                self.row += 1
                col = 0

            c.grid(row=self.row, column=col, columnspan=1)
            col += 1

        self.row += 1
