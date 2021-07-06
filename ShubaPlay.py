import tkinter as tk
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk
import pygame 
import glob 
import time 
from mutagen.mp3 import MP3
import os
import shelve

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
        self._tab_bar.add(self.playlist.frame, text='PlayList')
        self._tab_bar.grid(column=0, row=0)

class musicADT:
    def __init__(self):
        types = ('./**/*.wav', './**/*.mp3')
        self.files = []
        self.all = []
        self.current = 0
        self.checkpause = False
        self.start = False
        self.re = 0

        for files in types:
            self.files.extend(glob.glob(files, recursive=True))
            self.all.extend(glob.glob(files, recursive=True))

        pygame.init()
        # edit quality
        pygame.mixer.pre_init(frequency=48000, size=32, buffer=1024)
        pygame.mixer.init()
    
    def play(self):
        if self.check():
            pygame.mixer.music.stop()
        print("Playing - " + os.path.basename(self.files[self.current])[:-4])
        return os.path.basename(self.files[self.current])

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
        if self.current == len(self.files)-1:
            self.current = 0
        else:
            self.current += 1
        return self.play()

    def prev_track(self):
        if self.current == 0:
            self.current = len(self.files)-1
        else:
            self.current -=1
        return self.play()

    def rewind(self):
        pygame.mixer.music.rewind()
    
    def get_current(self):
        return self.files[self.current]

    def current_index(self):
        return self.current

    def change_current(self, curr):
        self.current = curr

    def printList(self):
        for file in self.files:
            print(os.path.basename(file)[:-4])

    def list_all(self):
        bef, aft = self.files[:self.current], self.files[self.current+1:] 
        for b in bef:
            bef[bef.index(b)] = os.path.basename(b)[:-4]
        for a in aft:
            aft[aft.index(a)] = os.path.basename(a)[:-4]
        return bef, aft

    def len_list(self):
        return len(self.files)

    def get_list(self):
        lis = []
        for file in self.files:
            lis.append(os.path.basename(file)[:-4])
        return lis
    
    def get_all(self):
        lis = []
        for file in self.all:
            lis.append(os.path.basename(file)[:-4])
        return lis

class ShubaPlay:

    def __init__(self, parent):
        # Create parent, frame
        self._parent = parent
        self.frame = tk.Frame(self._parent)

        # Create canvas, labels, listboxes
        self._canvas = tk.Canvas(self.frame, bg="#FCFBF7", height=250, width=300)

        self._label = tk.Label(self.frame, width=60, text="- - -")

        self._prevlist = tk.Listbox(self.frame, height=5, width=30)
        self._tracklist = tk.Listbox(self.frame, height=20, width=30)
        self._prevlist.insert(0, "Previous")
        self._tracklist.insert(0, "Next")
        self._prevlist.bind("<<ListboxSelect>>", self.click_song)
        self._tracklist.bind("<<ListboxSelect>>", self.click_song)

        # Create images
        # IMPORTANT ------------------------------------------------#
        self._piclist = os.listdir("img/shubapics")

        self._img = Image.open('img/shubapics/frame_00_delay-0.05s.jpg')
        self._img1 = self._img.resize((230,250),Image.ANTIALIAS) 
        self._img2 = ImageTk.PhotoImage(self._img1)
        self._imgtoken = 1
        
        self._canvas.create_image(30, 0, anchor="nw", tags="shuba", image=self._img2)
        # IMPORTANT ------------------------------------------------#
        self._playimg = Image.open('img/playbtn.jpg')
        self._play1 = self._playimg.resize((50,50),Image.ANTIALIAS) 
        self._play2 = ImageTk.PhotoImage(self._play1)

        self._pauseimg = Image.open('img/pausebtn.jpg')
        self._pause1 = self._pauseimg.resize((50,50),Image.ANTIALIAS) 
        self._pause2 = ImageTk.PhotoImage(self._pause1)

        self._previmg = Image.open('img/prevbtn.jpg')
        self._prev1 = self._previmg.resize((50,50),Image.ANTIALIAS) 
        self._prev2 = ImageTk.PhotoImage(self._prev1)

        self._nextimg = Image.open('img/nextbtn.jpg')
        self._next1 = self._nextimg.resize((50,50),Image.ANTIALIAS) 
        self._next2 = ImageTk.PhotoImage(self._next1)

        # Create buttons and buffer bar
        self._playbtn = tk.Button(self.frame, image=self._play2, padx=15, pady=15, command=self.play, borderwidth=0)
        self._prevbtn = tk.Button(self.frame, image=self._prev2, padx=15, pady=15, command=self.prev, borderwidth=0)
        self._nextbtn = tk.Button(self.frame, image=self._next2, padx=15, pady=15, command=self.next, borderwidth=0)

        self._buffer = ttk.Scale(self.frame, from_=0, orient="horizontal", length=300, cursor="sb_h_double_arrow", value=0)
        self._buffer.state(["disabled"])
        self._statbar = tk.Label(self.frame, width=60, text="-- / --")
        self.pos_widgets()

    def pos_widgets(self):
        # postition all widgets in frame
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
        # for list boxes, list of before and list of after current track
        b = 1
        rgb = 0
        a = 1

        if len(bef) != 0:
            if len(bef) > 4:
                bef = bef[-4:]

            for song in bef:
                self._prevlist.insert(b, song)
                if rgb == 0:
                    self._prevlist.itemconfig(b, {'bg':'#fff59a'})
                    rgb+=1
                else:
                    rgb = 0
                b+=1
        
        rgb = 0

        if len(aft) != 0:
            for song in aft:
                self._tracklist.insert(a, song)
                if rgb == 0:
                    self._tracklist.itemconfig(a, {'bg':'#fff59a'})
                    rgb+=1
                else:
                    rgb = 0
                a+=1

    def click_song(self, event):
        # when clicking song from listbox, find index to convert to song list index
        w = event.widget

        if w.curselection():
            index = int(w.curselection()[0])

            if index != 0:
                value = w.get(index)
                songs = music.get_list()
                ind = songs.index(value)
                music.change_current(ind)

                self.other_play(music.play())

    def buff(self, val):
        # slider func for buffer
        l = music.play()
        pygame.mixer.music.load(l)
        pygame.mixer.music.play(loops=0, start=int(self._buffer.get()))
    
    def reset_box(self):
        # reset both lists
        self._prevlist.delete(1,'end')
        self._tracklist.delete(1, 'end')

    def load_play(self, l):
        # load and play
        pygame.mixer.music.load(l)
        pygame.mixer.music.play()

    def other_play(self, play):
        # play func for click song, prev track and next track
        self._buffer.config(value=0)
        l = play
        self.load_play(l)

        self._playbtn.config(image=self._pause2)

        self.reset_box()
        bef, aft = music.list_all()
        self.insert_list(bef, aft)

        self._label['text'] = l
        music.start = True

    def play(self):
        # Main play func
        if not music.check() and music.start == False:
            global turn 
            turn = 0
            self._buffer.config(state="normal")
            self._buffer.bind("<ButtonRelease-1>", self.buff)

            # first time use
            l = music.play()
            self.load_play(l)
            self.play_time()

            self._playbtn.config(image=self._pause2)

            self.reset_box()
            bef, aft = music.list_all()
            self.insert_list(bef, aft)

            self._label['text'] = l
            music.start = True
        else:
            # pause and play func
            music.pause()  
            if music.checkpause:
                self._playbtn.config(image=self._play2)
            else: 
                self._playbtn.config(image=self._pause2)

    def play_time(self):
        global turn 
        if turn == 20:
            # grab elapsed time
            current_time = pygame.mixer.music.get_pos() / 1000 

            # convert to time
            convert_time = time.strftime('%M:%S', time.gmtime(current_time))

            # get song length
            song = music.files[music.current]

            # load song in mutagen
            song_muta = MP3(song)

            # song length
            global song_len
            song_len = song_muta.info.length

            # convert to song length
            convert_len = time.strftime('%M:%S', time.gmtime(song_len))

            current_time += 1    

            if int(self._buffer.get()) == int(song_len):
                # if the buffer = 100% and song is done then move to next song
                self._statbar.config(text=f'{convert_len} / {convert_len}')
                self._statbar.after(1000, self.next) 

            elif int(self._buffer.get()) == int(current_time):
                # if slider is moved = sync current time, then sync up buffer to current time
                buffer_pos = int(song_len)
                self._buffer.config(to=buffer_pos, value=int(current_time))

            else:
                if music.check():
                    self._playbtn.config(image=self._pause2)

                    buffer_pos = int(song_len)
                    self._buffer.config(to=buffer_pos, value=int(self._buffer.get()))

                    convert_time = time.strftime('%M:%S', time.gmtime(int(self._buffer.get())))
                    self._statbar.config(text=f'{convert_time} / {convert_len}')

                    next_time = int(self._buffer.get()) + 1
                    self._buffer.config(value=next_time)
                    
                    music.checkpause = False

            turn = 0

        self.gif_mover()
        turn+=1
        self._statbar.after(50, self.play_time)  

    def gif_mover(self):
        if music.check():
            # gif mover, iterate through jpgs
            self._canvas.delete("shuba")
            self._img = Image.open("img/shubapics/" + self._piclist[self._imgtoken])
            self._img1 = self._img.resize((230,250),Image.ANTIALIAS) 
            self._img2 = ImageTk.PhotoImage(self._img1)

            self._canvas.create_image(30, 0, anchor="nw", tags="shuba", image=self._img2)
            if self._imgtoken <= 90:
                self._imgtoken+=1
            else:
                self._imgtoken = 0

    def prev(self):
        if music.start == True:
            if music.re == 0 and music.check():
                self._buffer.config(value=0)
                music.rewind()
                music.re = 1
            else:
                self.other_play(music.prev_track())
                music.re = 0

    def next(self):
        if music.start == True:
            self.other_play(music.next_track())

class Playlist:

    def __init__(self, parent):
        # frames
        self._parent = parent
        self.frame = tk.Frame(self._parent)

        self.p_menu = tk.Frame(self.frame)
        self.p_list = tk.Frame(self.frame)  

        # status checks
        self._curr_list = "All songs"

        self.frame_status = False
        self.frame.rowconfigure(0, weight=1)
        for i in range(3):
            self.frame.columnconfigure(i, weight=1)

        #listboxes
        self._menu = tk.Listbox(self.p_menu, height=20, width=30)
        self._songlist = tk.Listbox(self.p_list, height=20, width=40)
        self._picklist = tk.Listbox(self.p_list, height=20, width=40)

        self._songlist.bind('<<ListboxSelect>>', self.click_song)
        self._picklist.bind('<<ListboxSelect>>', self.add_song)
        self._menu.bind("<<ListboxSelect>>", self.click_playlist)

        self._menu.insert(0, "All songs")

        shelf = bookshelf.get_keys()
        bookshelf.close()

        for key in shelf:
            self._menu.insert(self._menu.size(), key)

        self._allplists = self._menu.get(0, tk.END)

        self.insert_songs(music.get_list(), self._songlist)

        # other widgets
        self.ar_btn = tk.Button(self.frame, text="▶ Playlists", height=1, width=9, command=self.toggle_menu)

        self._title = tk.Label(self.p_list, text="All Songs")
        self._picktitle = tk.Label(self.p_list, text="All Songs")
        self._blank1 = tk.Label(self.p_list, height=2, width=4)
        self._savebtn = tk.Button(self.p_list, text="Save Changes", command=self.save_playlist)

        self._border = tk.Canvas(self.p_menu, bg="grey", height=400, width=1)
        self._blank = tk.Label(self.p_menu, width=2)
        self.add_plist_btn = tk.Button(self.p_menu, text="add +", command=self.create_playlist)
        self._plist_entry = tk.Entry(self.p_menu)
        
        self.pos_widgets()

        #############################
        bookshelf.delete_playlist()#
        #############################

    def toggle_menu(self):
        if self.frame_status:
            self.p_menu.grid_forget()
            self.frame_status = False
            self.ar_btn.config(text="▶ Playlists", width=9)
        else:
            self.frame_status = True
            self.p_menu.grid(row=0, column=2)
            self.ar_btn.config(text="◀", width=2)

    def pos_widgets(self):
        # listbox placements
        self.p_list.grid(row=0, column=0)
        self._songlist.grid(row=1, column=0, sticky='nsew')

        # labels
        self._title.grid(row=0, column=0)

        # buttons and other widgets
        self.ar_btn.grid(row=0, column=2, sticky='ne')

        self._border.grid(row=0, column=0, rowspan=8, sticky='w')
        self._blank.grid(row=3, column=2)

        self._plist_entry.grid(row=1, column=3)
        self.add_plist_btn.grid(row=1, column=4)

        self._menu.grid(row=3, column=3, columnspan=2, rowspan=5, sticky='e')

    def insert_songs(self, songs, lst):
        # for list boxes, list of before and list of after current track
        b = 0
        print("HEY ---")
        print(songs)
        for s in songs:
            if s[-4:] != ".mp3":
                s = s + ".mp3"
            song_muta = MP3(s)
            song_len = song_muta.info.length
            convert_len = time.strftime('%M:%S', time.gmtime(song_len))

            lst.insert(b, convert_len + "             " + s)

            if b % 2 != 0:
                lst.itemconfig(b, {'bg':'#fff59a'})
            b+=1

    def click_playlist(self, event):
        # when clicking playlist from listbox
        w = event.widget

        if w.curselection():
            index = int(w.curselection()[0])
            value = w.get(index)

            if value != self._curr_list:
                self._songlist.delete(0,'end')
                print("the index is " + str(index))
                
                if index == 0:
                    self.insert_songs(music.get_all(), self._songlist)
                else:
                    plist = bookshelf.access_playlist(value)
                    self.insert_songs(plist, self._songlist)
                self._curr_list = value
                self._title.config(text=self._curr_list)

    def create_playlist(self):
        global input
        input = self._plist_entry.get()

        if input:
            if input not in self._allplists:

                # save song into the shelf
                bookshelf.save_playlist(input, [])

                # blank the songlist
                self._songlist.delete(0,'end')

                self._title.config(text=input)
                self._curr_list = input
                print("Created new playlist: " + input)

                self.change_playlist()
                self._songlist.unbind('<<ListboxSelect>>')
                self._songlist.bind('<Double-1>', self.remove_song)
            else:
                print("Name already taken")

    def change_playlist(self):
        self._picktitle.grid(row=0, column=2)
        self._picklist.grid(row=1, column=2, sticky='nsew')
        self._blank1.grid(row=3)
        self._savebtn.grid(row=4, column=1, sticky='ne')

        self.toggle_menu()
        self.insert_songs(music.get_list(), self._picklist)
        self.ar_btn.grid_forget()

    def save_playlist(self):
        self._blank1.grid_forget()
        self._picktitle.grid_forget()
        self._savebtn.grid_forget()
        self._picklist.grid_forget()

        self._picklist.delete(0, 'end')
        self._songlist.delete(0, 'end')

        self.ar_btn.grid(row=0, column=2, sticky='ne')

        self._songlist.unbind('<Double-1>')
        self._songlist.bind('<<ListboxSelect>>', self.click_song)

        global input 
        # add playlist name into the menu
        self._menu.insert(self._menu.size(), input)

        songs = bookshelf.access_playlist(self._curr_list)

        self.insert_songs(songs, self._songlist)

    def click_song(self, event):
        # when clicking song from listbox, find index to convert to song list index
        w = event.widget

        if w.curselection():
            index = int(w.curselection()[0])

            if self._curr_list != "All songs":
                music.files = bookshelf.access_playlist(self._curr_list)
            else:
                music.files = music.all
                
            music.change_current(index)

            app.shubaplay.other_play(music.play())

    
    def add_song(self, event):
        # when clicking playlist from listbox
        w = event.widget

        if w.curselection():
            index = int(w.curselection()[0])
            value = w.get(index)
            current_plist = bookshelf.access_playlist(self._curr_list) 

            if value not in current_plist:
                value = value[18:]
                print(value)
                current_plist.append(value)
                bookshelf.save_playlist(self._curr_list, current_plist)
                self._songlist.insert(self._songlist.size(), value)

    def remove_song(self, event):
        # when clicking playlist from listbox
        w = event.widget

        if w.curselection():
            index = int(w.curselection()[0])
            value = w.get(index)
            print(value)
            current_plist = bookshelf.access_playlist(self._curr_list) 

            current_plist.remove(value)
            bookshelf.save_playlist(self._curr_list, current_plist)
            self._songlist.delete(index)


class Bookshelf:
    
    def __init__(self):
        self.name = "Bookshelf"

    def get_keys(self):
        st = shelve.open(self.name)
        return st.keys()
    
    def close(self):
        st = shelve.open(self.name)
        st.close()

    def access_playlist(self, name):
        st = shelve.open(self.name)
        temp = st[name]
        st.close()
        return temp

    def save_playlist(self, name, value):
        # value is a list, playlist
        st = shelve.open(self.name, writeback=True)
        st[name] = value
        st.close()
    
    def delete_playlist(self):
        st = shelve.open(self.name)
        for key in self.get_keys():
            del st[key]
        st.close()

bookshelf = Bookshelf()
music = musicADT()
app = Main()
app.root.mainloop()
