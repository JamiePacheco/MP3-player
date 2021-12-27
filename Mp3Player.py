from tkinter import *
from typing import List
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Mp3 Player")
root.geometry("400x350")
root.config(bg="#685E69")

#858585 - light grey
#685E69 - dark grey

#Initalize Pygame Mixer
pygame.mixer.init()

global stopped 
stopped = False

#Grab song playing time information
def play_time():

    global current_time, song_length

    if stopped:
        return
    #Grab elapsed time for song
    current_time = pygame.mixer.music.get_pos()/1000

    #throw up temp label
    #slider_label.config(text=f"Slider: {int(my_slider.get())} and Song Pos:{int(current_time)}")

    converted_time = time.strftime("%M:%S", time.gmtime(current_time))

    #get the next song
    song = song_box.get(ACTIVE)
    #add directory and file extension to song name
    song = f"c:/Users{song}.mp3"
    #get song length using mutagen

    song_mut = MP3(song)
    song_length = song_mut.info.length

    converted_time_mut = time.strftime("%M:%S", time.gmtime(song_length))

    #increase current time by one second
    current_time += 1

    if int(my_slider.get() == int(song_length)):
        status_bar.config(text=f"{converted_time_mut} / {converted_time_mut}")
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        #slider hasn't been moved
        
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

        status_bar.config(text=f"{converted_time} / {converted_time_mut}")
    else:
        #slider has been moved   
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        #Change the time
        converted_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))

        status_bar.config(text=f"{converted_time} / {converted_time_mut}")

        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    status_bar.after(1000, play_time)

    #Change the time
    #status_bar.config(text=f"{converted_time} / {converted_time_mut}")

    #updateslider position value tp current song position
    #my_slider.config(value=int(current_time))

    #slider_position = int(song_length)
    #my_slider.config(to=slider_position, value=int(current_time))

    #update time
    
#add song function 
def add_song():

    #prompt user to open file from music directory
    song = filedialog.askopenfilename(initialdir="C\\Users", title="Choose a song", filetypes = (("mp3 Files", "*.mp3"),))

    #remove certain text attributes
    song = song.replace("C:/Users/jamie/Music/", "")
    song = song.replace(".mp3","")

    #insert file in text box
    song_box.insert(END, song)

#add multiple songs to the playlist
def add_songs():
    songs = filedialog.askopenfilenames(initialdir="C\\Users", title="Choose a song", filetypes = (("mp3 Files", "*.mp3"),))

    #loop through song list
    for song in songs:
        song = song.replace("C:/Users", "")
        song = song.replace(".mp3","")
        song_box.insert(END, song)

#play selected song
def play():
    #set stopped to false so song can play
    global stopped
    stopped = False

    song = song_box.get(ACTIVE)
    song = f"c:/Users{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    #insert time length
    play_time()

    #update slider to position
    #slider_position = int(song_length)
    #my_slider.config(to=slider_position, value=0)



#stop playing current song

def stop():
    status_bar.config(text = "")
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    #remove timer from bottom right
    status_bar.config(text = "")

    #Set stop Variable to True
    global stopped
    stopped = True


#Creat global pause variable
global paused
paused = False

def next_song():
    #reset status bar
    status_bar.config(text = "")
    my_slider.config(value=0)

    #get current song index
    next_one = song_box.curselection()
    next_one = next_one[0] + 1

    #get the next song
    song = song_box.get(next_one)
    #add directory and file extension to song name
    song = f"c:/Users{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #move active bar in list box
    song_box.selection_clear(0,END)
    #activate new song
    song_box.activate(next_one)
    song_box.select_set(next_one, last = None)
    
def previous_song():
    #reset status bar
    status_bar.config(text = "")
    my_slider.config(value=0)

    #get current song index
    previous_one = song_box.curselection()
    previous_one = previous_one[0] - 1

    #get the next song
    song = song_box.get(previous_one)
    #add directory and file extension to song name
    song = f"c:/Users{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #move active bar in list box
    song_box.selection_clear(0,END)
    #activate new song
    song_box.activate(previous_one)
    song_box.select_set(previous_one, last = None)
    
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

#pause and unpause the current song
def pause(is_paused):
    global paused
    paused = is_paused

    #Checks if pause is true
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def slide(xS):
    #slider_label.config(text=f"{int(my_slider.get())} of {int(song_length)}")

    song = song_box.get(ACTIVE)
    song = f"c:/Users{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops= 0, start=int(my_slider.get()))



#Create Playlist Box
song_box = Listbox(root, bg = "black", fg = "green", width=60, selectbackground="green", selectforeground="black", borderwidth=0)
song_box.pack(padx=20, pady=20)


#Create user control frame
controls_frame = Frame(root)
controls_frame.pack()

#making player control button

back_button = Button(controls_frame, text="back", command = previous_song)
forward_button = Button(controls_frame, text="forward", command = next_song)
pause_button = Button(controls_frame, text = "pause", command = lambda: pause(paused))
play_button = Button(controls_frame, text = "play", command=play)
stop_button = Button(controls_frame, text = "stop", command = stop)

#griding control buttons

back_button.grid(column=1,row=0)
forward_button.grid(column=2,row=0)
pause_button.grid(column=3,row=0)
play_button.grid(column=4,row=0)
stop_button.grid(column=5, row=0)

#create a menu 
my_menu = Menu(root)
root.config(menu=my_menu)

#add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add A Song To Playlist", command = add_song)

#add multiple songs
add_song_menu.add_command(label="Add Multiple Songs To Playlist", command = add_songs)

# Create Delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label = "Delete song from playlist", command = delete_song)
remove_song_menu.add_command(label = "Delete all songs from playlist", command = delete_songs)

# Create Status Bar
status_bar = Label(root, text="", bd =1, relief=GROOVE, anchor=E, bg = "#858585", border=1)
status_bar.pack(fill=X, side = BOTTOM, ipady=2)

#create a slider
my_slider = ttk.Scale(root, from_= 0, to = 100, orient = HORIZONTAL, value = 0, command = slide, length = 360)
my_slider.pack(pady=20)

#Creater slider label
#slider_label = Label(root, text = "")
#slider_label.pack(pady=10)

root.mainloop()