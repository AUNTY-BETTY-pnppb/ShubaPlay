import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame 
import glob 
import time 
from mutagen.mp3 import MP3
import os

class Main:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ShubaPlay")
        self.style = ttk.Style(self.root)
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        self._tab_bar = tk.ttk.Notebook(self.root, style='lefttab.TNotebook')
        self.playlist = Playlist(self._tab_bar)
        self.shubaplay = ShubaPlay(self._tab_bar)
        self.tabControl()

    def tabControl(self):
        self._tab_bar.add(self.shubaplay.frame, text='ShubaPlay')
        self._tab_bar.add(self.playlist.frame, text='ShubaList')
        self._tab_bar.grid(column=0, row=0)

class musicADT:
    def __init__(self):
        types = ('./**/*.wav', './**/*.mp3')
        self._files = []
        self._current = 0
        self.checkpause = False
        self.start = False
        self.re = 0

        for files in types:
            self._files.extend(glob.glob(files, recursive=True))

        pygame.init()
        # edit quality
        pygame.mixer.pre_init(frequency=48000, size=32, buffer=1024)
        pygame.mixer.init()
    
    def play(self):
        if self.check():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(self._files[self._current])
        pygame.mixer.music.play()
        print("Playing - " + os.path.basename(self._files[self._current])[:-4])
        return os.path.basename(self._files[self._current])[:-4]

    def pause(self):
        if not self.checkpause:
            pygame.mixer.music.pause()
            self.checkpause = True
        else:
            pygame.mixer.music.unpause()
            self.checkpause = False
    
    def stop(self):
        if self.check():
            pygame.mixer.music.stop()

    def check(self):
        if pygame.mixer.music.get_busy():
            return True
        else:
            return False

    def next_track(self):
        if self._current == len(self._files)-1:
            self._current = 0
        else:
            self._current += 1
        return self.play()

    def prev_track(self):
        if self._current == 0:
            self._current = len(self._files)-1
        else:
            self._current -=1
        return self.play()

    def rewind(self):
        pygame.mixer.music.rewind()

    def printList(self):
        for file in self._files:
            if file == self._files[self._current]:
                print("-" + os.path.basename(self._files[file])[:-4])
            else:
                print(os.path.basename(self._files[file])[:-4])

    def list_all(self):
        bef, aft = self._files[:self._current], self._files[self._current+1:] 
        for b in bef:
            bef[bef.index(b)] = os.path.basename(b)[:-4]
        for a in aft:
            aft[aft.index(a)] = os.path.basename(a)[:-4]
        return bef, aft

class ShubaPlay:

    def __init__(self, parent):
        self._parent = parent
        self.frame = tk.Frame(self._parent)
        self._prog_var = tk.IntVar()
        self._canvas = tk.Canvas(self.frame, bg="white", height=250, width=300)
        self._label = tk.Label(self.frame, width=60, text="- - -")
        self._prevlist = tk.Listbox(self.frame, height=5, width=30)
        self._tracklist = tk.Listbox(self.frame, height=20, width=30)
        self._prevlist.insert(0, "Previous")
        self._tracklist.insert(0, "Next")
        self._playbtn = tk.Button(self.frame, text='Play', padx=15, pady=15, command=self.play)
        self._prevbtn = tk.Button(self.frame, text='Prev', padx=15, pady=15, command=self.prev)
        self._nextbtn = tk.Button(self.frame, text='Next', padx=15, pady=15, command=self.next)
        self._statbar = tk.Label(self.frame, width=60, text="hey what do you mean?")
        self.pos_widgets()

    def pos_widgets(self):
        self._canvas.grid(row=0, column=1, columnspan=7, rowspan=2)
        self._label.grid(row=2, column=1, columnspan=7)
        self._prevlist.grid(row=0, column=8)
        self._tracklist.grid(row=1, column=8, rowspan=4)
        self._prevbtn.grid(row=3, column=3, sticky="n")
        self._playbtn.grid(row=3, column=4, sticky="n")
        self._nextbtn.grid(row=3, column=5, sticky="n")
        self._statbar.grid(row=4, column=1, columnspan=7, sticky="s")

    def insert_list(self, bef, aft):
        b = 1
        a = 1
        if len(bef) != 0:
            if len(bef) > 4:
                bef = bef[-4:]

            for song in bef:
                self._prevlist.insert(b, song)
                b+=1

        if len(aft) != 0:
            for song in aft:
                self._tracklist.insert(a, song)
                a+=1
    
    def reset_box(self):
        self._prevlist.delete(1,'end')
        self._tracklist.delete(1, 'end')

    def play(self):
        if not music.check() and music.start == False:
            l = music.play()
            self.reset_box()
            bef, aft = music.list_all()
            self.insert_list(bef, aft)
            self._label['text'] = l
            music.start = True
        else:
            music.pause()    

    def prev(self):
        if music.re == 0 and music.check():
            music.rewind()
            music.re = 1
        else:
            l = music.prev_track()
            self.reset_box()
            bef, aft = music.list_all()
            self.insert_list(bef, aft)
            self._label['text'] = l
            music.re = 0

    def next(self):
        l = music.next_track()
        self.reset_box()
        bef, aft = music.list_all()
        self.insert_list(bef, aft)
        self._label['text'] = l

class Playlist:

    def __init__(self, parent):
        self._parent = parent
        self.frame = tk.Frame(self._parent)

music = musicADT()
app = Main()
app.root.mainloop()
