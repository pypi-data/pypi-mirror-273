import pygame
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *


class Timer(QMainWindow):
    def __init__(self):
        super(Timer, self).__init__()
        uic.loadUi("timer.ui", self)

        self.time_label = self.findChild(QLabel, "time")
        self.ten_minutes_button = self.findChild(QPushButton, "ten_minutes")
        self.pause_button = self.findChild(QPushButton, "pause_button")
        self.resume_button = self.findChild(QPushButton, "resume_button")
        self.reset_button = self.findChild(QPushButton, "reset_button")

        self.ten_minutes_button.clicked.connect(self.start_ten_minutes_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.resume_button.clicked.connect(self.resume_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        pygame.mixer.init()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.update_button_states(timer_running=False)

        self.show()

    def update_button_states(self, timer_running):
        self.ten_minutes_button.setEnabled(not timer_running)

        self.pause_button.setEnabled(timer_running)
        self.resume_button.setEnabled(timer_running)
        self.reset_button.setEnabled(timer_running)

    def start_timer(self, time_seconds):
        self.time_left = time_seconds
        self.timer.start(1000)
        self.update_button_states(timer_running=True)
        self.resume_button.setEnabled(False)

    def start_ten_minutes_timer(self):
        self.start_timer(600)

    def update_time(self):
        if self.time_left:
            minutes, seconds = divmod(self.time_left, 60)
            self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
            self.time_left -= 1
        else:
            self.timer.stop()
            self.play_sound()

    def pause_timer(self):
        self.timer.stop()
        self.resume_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def resume_timer(self):
        self.timer.start(1000)
        self.resume_button.setEnabled(False)
        self.pause_button.setEnabled(True)

    def reset_timer(self):
        self.timer.stop()
        self.time_left = 0
        self.time_label.setText("00:00")
        self.update_button_states(timer_running=False)

    def play_sound(self):
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play()
        self.reset_timer()


def main():
    app = QApplication([])
    window = Timer()
    app.exec_()


if __name__ == "__main__":
    main()
