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
        self._canvas = tk.Canvas(self.frame, bg="blue", height=250, width=300)
        self._prevlist = tk.Listbox(self.frame, height=20, width=30)
        self._tracklist = tk.Listbox(self.frame, height=20, width=30)
        self._playbtn = tk.Button(self.frame, text='Play', padx=25, pady=15)
        self._prevbtn = tk.Button(self.frame, text='Prev', padx=25, pady=15)
        self._nextbtn = tk.Button(self.frame, text='Next', padx=25, pady=15)
        self.pos_widgets()

    def pos_widgets(self):
        self._canvas.grid(row=1, column=1, columnspan=3)
        self._tracklist.grid(row=1, column=4, rowspan=3)
        self._prevbtn.grid(row=2, column=1)
        self._playbtn.grid(row=2, column=2)
        self._nextbtn.grid(row=2, column=3)

class Playlist:

    def __init__(self, parent):
        self._parent = parent
        self.frame = tk.Frame(self._parent)

app = Main()
app.root.mainloop()