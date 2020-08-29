import tkinter as tk
from tkinter import simpledialog


class InfoBox(simpledialog.Dialog):
    def __init__(self, master, infos):
        self.infos = infos
        super().__init__(master)

    def body(self, master):
        for i, info in enumerate(self.infos):
            key, value = info.split(';')
            tk.Label(master, text=key).grid(row=i, column=0, sticky='w')
            tk.Label(master, text=value).grid(row=i, column=1, sticky='w')

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok)
        w.pack(side='bottom', padx=5, pady=5)

        self.bind("<Return>", self.ok)

        box.pack()
