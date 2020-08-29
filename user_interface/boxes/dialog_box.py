import tkinter as tk
from tkinter import simpledialog


class DialogBox(simpledialog.Dialog):
    def __init__(self, master, prompt1, prompt2=None, info=None):
        self.prompt1 = prompt1
        self.prompt2 = prompt2
        self.info = info
        super().__init__(master)

    def body(self, master):
        self.item_key = None
        self.item_value = None

        if self.info:
            tk.Label(master, text=self.info).grid(row=0, columnspan=2)

        tk.Label(master, text=self.prompt1).grid(row=2)
        self.entry1 = tk.Entry(master)
        self.entry1.grid(row=2, column=1)

        if self.prompt2 != None:
            tk.Label(master, text=self.prompt2).grid(row=3)
            self.entry2 = tk.Entry(master)
            self.entry2.grid(row=3, column=1)

    def apply(self):
        self.item_key = self.entry1.get()
        if self.prompt2 != None:
            self.item_value = self.entry2.get()
