import tkinter as tk
from tkinter import PhotoImage, ttk
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
        print("Playing - " + os.path.basename(self._files[self._current])[:-4])
        return os.path.basename(self._files[self._current])

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
    
    def get_current(self):
        return self._files[self._current]

    def printList(self):
        for file in self._files:
            if file == self.get_current():
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

        self._canvas = tk.Canvas(self.frame, bg="white", height=250, width=300)

        self._label = tk.Label(self.frame, width=60, text="- - -")

        self._prevlist = tk.Listbox(self.frame, height=5, width=30)
        self._tracklist = tk.Listbox(self.frame, height=20, width=30)
        self._prevlist.insert(0, "Previous")
        self._tracklist.insert(0, "Next")

        self._playimg = Image.open('img/playbtn.jpg')
        self._play1 = self._playimg.resize((50,50),Image.ANTIALIAS) 
        self._play2 = ImageTk.PhotoImage(self._play1)

        self._previmg = Image.open('img/prevbtn.jpg')
        self._prev1 = self._previmg.resize((50,50),Image.ANTIALIAS) 
        self._prev2 = ImageTk.PhotoImage(self._prev1)

        self._nextimg = Image.open('img/nextbtn.jpg')
        self._next1 = self._nextimg.resize((50,50),Image.ANTIALIAS) 
        self._next2 = ImageTk.PhotoImage(self._next1)

        self._playbtn = tk.Button(self.frame, image=self._play2, padx=15, pady=15, command=self.play, borderwidth=0)
        self._prevbtn = tk.Button(self.frame, image=self._prev2, padx=15, pady=15, command=self.prev, borderwidth=0)
        self._nextbtn = tk.Button(self.frame, image=self._next2, padx=15, pady=15, command=self.next, borderwidth=0)

        self._buffer = ttk.Scale(self.frame, from_=0, orient="horizontal", length=300, cursor="sb_h_double_arrow", value=0)
        self._buffer.bind("<ButtonRelease-1>", self.buff)
        self._statbar = tk.Label(self.frame, width=60, text="-- / --")
        self.pos_widgets()

    def pos_widgets(self):
        self._canvas.grid(row=0, column=1, columnspan=7, rowspan=2)
        self._label.grid(row=2, column=1, columnspan=7)
        self._prevlist.grid(row=0, column=8)
        self._tracklist.grid(row=1, column=8, rowspan=5)
        self._prevbtn.grid(row=3, column=3, sticky="n")
        self._playbtn.grid(row=3, column=4, sticky="n")
        self._nextbtn.grid(row=3, column=5, sticky="n")
        self._buffer.grid(row=4, column=2, columnspan=5)
        self._statbar.grid(row=5, column=1, columnspan=7, sticky="n")

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

    def buff(self, val):
        l = music.play()
        pygame.mixer.music.load(l)
        pygame.mixer.music.play(loops=0, start=int(self._buffer.get()))
    
    def reset_box(self):
        self._prevlist.delete(1,'end')
        self._tracklist.delete(1, 'end')

    def load_play(self, l):
        pygame.mixer.music.load(l)
        pygame.mixer.music.play()

    def play(self):
        if not music.check() and music.start == False:
            l = music.play()
            self.load_play(l)
            self.play_time()

            self.reset_box()
            bef, aft = music.list_all()
            self.insert_list(bef, aft)

            self._label['text'] = l
            music.start = True
        else:
            music.pause()  

    def play_time(self):
        # grab elapsed time
        current_time = pygame.mixer.music.get_pos() / 1000 

        # convert to time
        convert_time = time.strftime('%M:%S', time.gmtime(current_time))

        # get song length
        song = music._files[music._current]

        # load song in mutagen
        song_muta = MP3(song)

        # song length
        global song_len
        song_len = song_muta.info.length

        # convert to song length
        convert_len = time.strftime('%M:%S', time.gmtime(song_len))

        current_time += 1

        if int(self._buffer.get()) == int(song_len):
            self._statbar.config(text=f'{convert_len} / {convert_len}')
            self._statbar.after(1000, self.next) 

        elif int(self._buffer.get()) == int(current_time):
            buffer_pos = int(song_len)
            self._buffer.config(to=buffer_pos, value=int(current_time))

        else:
            buffer_pos = int(song_len)
            self._buffer.config(to=buffer_pos, value=int(self._buffer.get()))

            convert_time = time.strftime('%M:%S', time.gmtime(int(self._buffer.get())))

            self._statbar.config(text=f'{convert_time} / {convert_len}')

            next_time = int(self._buffer.get()) + 1
            self._buffer.config(value=next_time)

        self._statbar.after(1000, self.play_time)  

    def prev(self):
        if music.re == 0 and music.check():
            self._buffer.config(value=0)
            music.rewind()
            music.re = 1
        else:
            self._buffer.config(value=0)
            l = music.prev_track()
            self.load_play(l)

            self.reset_box()
            bef, aft = music.list_all()
            self.insert_list(bef, aft)
            self._label['text'] = l
            music.re = 0

    def next(self):
        self._buffer.config(value=0)
        l = music.next_track()
        self.load_play(l)
        
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
