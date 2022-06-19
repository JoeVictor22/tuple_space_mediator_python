import tkinter as tk


master = tk.Tk()
sensor = None

buffer_len = 25


def create_message(messages):
    final_txt = ""

    for message in messages:
        final_txt += f"{message}\n"
    return final_txt


def start(sensor_alvo):
    global sensor
    sensor = sensor_alvo

    def is_int(ob):
        try:
            if ob and ob != "" and type(int(ob.get())) is int:
                return True
        except:
            return False

        return False

    def set_min():
        if is_int(entry1):
            sensor.set_min(int(entry1.get()))
            update_labels()

    def set_max():
        if is_int(entry2):
            sensor.set_max(int(entry2.get()))
            update_labels()

    def set_value():
        if is_int(entry3):
            sensor.value = int(entry3.get())
            update_labels()

    def set_active():
        sensor.active = not sensor.active
        update_labels()

    def set_random():
        sensor.random = not sensor.random
        update_labels()

    min_lim, max_lim, value, n_calls, random, active = (
        tk.StringVar(),
        tk.StringVar(),
        tk.StringVar(),
        tk.StringVar(),
        tk.StringVar(),
        tk.StringVar(),
    )

    def update_labels():
        min_lim.set(f"Minimo: {sensor.min_target}")
        max_lim.set(f"Máximo: {sensor.max_target}")
        value.set(f"Leitura: {sensor.value}")
        n_calls.set(f"Acionamentos: {sensor.calls}")
        random.set(("Ativado" if sensor.random else "Desativado"))
        active.set(("Ativado" if sensor.active else "Desativado"))

    update_labels()

    idx = 0
    # input min
    label1 = tk.Label(master, textvariable=min_lim)
    label1.config(font=("helvetica", 10))
    label1.grid(row=0, column=idx, columnspan=1)
    # grid
    entry1 = tk.Entry(master)
    entry1.grid(row=1, column=idx, columnspan=1)
    # grid
    submit1 = tk.Button(master, text="Aceitar", command=set_min, bd=3)
    submit1.grid(row=2, column=idx, columnspan=1)

    idx += 1
    # input max
    label2 = tk.Label(master, textvariable=max_lim)
    label2.config(font=("helvetica", 10))
    label2.grid(row=0, column=idx, columnspan=1)
    # grid
    entry2 = tk.Entry(master)
    entry2.grid(row=1, column=idx, columnspan=1)
    # grid
    submit2 = tk.Button(master, text="Aceitar", command=set_max, bd=3)
    submit2.grid(row=2, column=idx, columnspan=1)

    idx += 1
    # valor atual
    label3 = tk.Label(master, textvariable=value)
    label3.config(font=("helvetica", 10))
    label3.grid(row=0, column=idx, columnspan=1)
    # grid
    entry3 = tk.Entry(master)
    entry3.grid(row=1, column=idx, columnspan=1)
    # grid
    submit3 = tk.Button(master, text="Aceitar", command=set_value, bd=3)
    submit3.grid(row=2, column=idx, columnspan=1)

    idx += 1
    # gerar aleatorio/button
    submit5 = tk.Button(master, text="Leitura aleatória", command=set_random, bd=3)
    submit5.grid(row=2, column=idx, columnspan=1)
    label5 = tk.Label(master, textvariable=random)
    label5.config(font=("helvetica", 10))
    label5.grid(row=0, column=idx, columnspan=1)

    idx += 1
    # ativar
    submit8 = tk.Button(master, text="Ativar/Desativar", command=set_active, bd=3)
    submit8.grid(row=2, column=idx, columnspan=1)
    label8 = tk.Label(master, textvariable=active)
    label8.config(font=("helvetica", 10))
    label8.grid(row=0, column=idx, columnspan=1)

    # leitura atual
    label6 = tk.Label(master, textvariable=value)
    label6.config(font=("helvetica", 20))
    label6.grid(row=3, column=0, columnspan=5)

    # acionamentos
    label7 = tk.Label(master, textvariable=n_calls)
    label7.config(font=("helvetica", 20))
    label7.grid(row=4, column=0, columnspan=5)

    # info
    label8 = tk.Label(master, text=f"Name: {sensor.name}")
    label8.config(font=("helvetica", 20))
    label8.grid(row=5, column=0, columnspan=2)

    label9 = tk.Label(master, text=f"Topic: {sensor.topic_name}")
    label9.config(font=("helvetica", 20))
    label9.grid(row=5, column=2, columnspan=2)

    label10 = tk.Label(
        master, text=f"Parameter: {sensor.monitor_types[sensor.monitor]}"
    )
    label10.config(font=("helvetica", 20))
    label10.grid(row=5, column=4, columnspan=2)

    text_box = tk.Text(master, height=buffer_len, width=100)
    text_box.grid(row=6, column=0, columnspan=10, rowspan=2)

    def set_text(message):
        text_box.delete(1.0, "end")
        text_box.insert("end", message)

    while True:
        update_labels()
        master.update()
        sensor.update()
        set_text(create_message(sensor.buffer[-buffer_len:]))
