import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Main:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ShubaPlay")
        self._tab_bar = tk.ttk.Notebook(self.root)
        self.playlist = Playlist(self._tab_bar)
        self.shubaplay = ShubaPlay(self._tab_bar)
        self.tabControl()

    def tabControl(self):
        self._tab_bar.add(self.shubaplay.frame, text='ShubaPlay')
        self._tab_bar.add(self.playlist.frame, text='Playlist')
        self._tab_bar.grid(column=0, row=0)

class ShubaPlay:

    def __init__(self, parent):
        self._parent = parent
        self.frame = tk.Frame(self._parent)
        self._prog_var = tk.IntVar()
        self._canvas = tk.Canvas(self.frame, bg="blue", height=250, width=300)
        self._buffer = ttk.Progressbar(self.frame, orient="horizontal", length=280, maximum=100, mode="determinate", var=self._prog_var)
        self._prevlist = tk.Listbox(self.frame, bg="green", height=5, width=30)
        self._tracklist = tk.Listbox(self.frame, bg="red", height=20, width=30)
        self._playbtn = tk.Button(self.frame, text='Play', padx=25, pady=15)
        self._prevbtn = tk.Button(self.frame, text='Prev', padx=25, pady=15)
        self._nextbtn = tk.Button(self.frame, text='Next', padx=25, pady=15)
        self.pos_widgets()

    def pos_widgets(self):
        self._canvas.grid(row=0, column=1, columnspan=3, rowspan=2)
        self._buffer.grid(row=2, column=1, columnspan=3)
        self._prevlist.grid(row=0, column=4)
        self._tracklist.grid(row=1, column=4, rowspan=3)
        self._prevbtn.grid(row=3, column=1, sticky="n")
        self._playbtn.grid(row=3, column=2, sticky="n")
        self._nextbtn.grid(row=3, column=3, sticky="n")

class Playlist:

    def __init__(self, parent):
        self._parent = parent
        self.frame = tk.Frame(self._parent)

app = Main()
app.root.mainloop()
