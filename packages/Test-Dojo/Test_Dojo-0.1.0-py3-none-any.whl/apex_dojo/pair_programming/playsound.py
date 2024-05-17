import threading
from tkinter import messagebox

import pygame


def play_sound_thread():
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def play_sound_and_show_message():
    threading.Thread(target=play_sound_thread).start()
    messagebox.showinfo("Time's Up!", "The timer has expired!")
