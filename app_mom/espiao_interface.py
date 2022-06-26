import tkinter as tk


master = tk.Tk()
espiao = None

buffer_len = 25


def create_message(messages):
    final_txt = ""

    for message in messages:
        final_txt += f"{message}\n"
    return final_txt


def start(espiao_alvo):
    global espiao
    espiao = espiao_alvo

    def is_str(ob):
        try:
            if ob and ob != "" and type(str(ob.get())) is str:
                return True
        except:
            return False

        return False

    def add_new_msg():
        if is_str(entry1):
            msg = str(entry1.get())
            espiao.add_new_msg(msg)
            espiao.insert_message(msg)
            update_labels()

    def update_labels():
        pass
        # min_lim.set(f"Minimo: {espiao.min_target}")

    update_labels()

    idx = 0
    # input min
    label1 = tk.Label(master, text="Mensagem a monitorar")
    label1.config(font=("helvetica", 10))
    label1.grid(row=0, column=idx, columnspan=1)
    # grid
    entry1 = tk.Entry(master)
    entry1.grid(row=1, column=idx, columnspan=1)
    # grid
    submit1 = tk.Button(master, text="Aceitar", command=add_new_msg, bd=3)
    submit1.grid(row=2, column=idx, columnspan=1)

    text_box = tk.Text(master, height=buffer_len, width=100)
    text_box.grid(row=6, column=0, columnspan=10, rowspan=2)

    def set_text(message):
        text_box.delete(1.0, "end")
        text_box.insert("end", message)

    while True:
        update_labels()
        master.update()
        espiao.update()
        set_text(create_message(espiao.buffer[-buffer_len:]))
