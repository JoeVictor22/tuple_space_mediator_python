import tkinter as tk


def select_choice():
    pass


def create_choices():
    global topics, choose
    choose = []

    row = OPTIONS_ROW
    col = 1
    for value in topics:
        var = tk.BooleanVar()
        choose.append(var)
        c = tk.Checkbutton(
            master,
            text=value,
            variable=var,
            onvalue=1,
            offvalue=0,
            command=select_choice,
        )

        if col == 7:
            row += 1
            col = 1

        c.grid(row=row, column=col, columnspan=1)
        col += 1


OPTIONS_ROW = 5
TEXT_COL = 10
topics = []
choose = []
master = tk.Tk()
client = None
buffer = []
buffer_len = 50


def create_message(messages):
    final_txt = ""

    for message in messages:
        final_txt += f"{message}\n"
    return final_txt


def start(cliente):
    global client, topics, buffer
    client = cliente
    topics = client.broker_topics

    button_reset = tk.Button(
        master, text="Resetar tópicos", command=create_choices, bd=3
    )
    button_reset.grid(row=OPTIONS_ROW, column=0, columnspan=1)

    text_box = tk.Text(master, height=50, width=120)
    text_box.grid(row=0, column=0, columnspan=TEXT_COL, rowspan=OPTIONS_ROW)

    def set_text(message):
        text_box.delete(1.0, "end")
        text_box.insert("end", message)

    while True:
        topics = client.broker_topics
        client.update()
        master.update()
        client.set_topics(
            [topics[idx] for idx, _ in enumerate(choose) if choose[idx].get()]
        )
        set_text(create_message(cliente.buffer[-buffer_len:]))
