import tkinter as tk

from PIL import Image, ImageTk


class ImageFrame(tk.Frame):
    def __init__(self, master, image_path, *pargs):
        tk.Frame.__init__(self, master, *pargs)

        self.image = Image.open(image_path)
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)
