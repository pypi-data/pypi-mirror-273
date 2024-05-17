import os.path
import threading
import time
import tkinter as tk

from apex_dojo.pair_programming.button_controls import disable_controls, enable_controls
from apex_dojo.pair_programming.playsound import play_sound_and_show_message

timer_running = False
timer_paused = False
remaining_time = 0
current_timer = None


def update_timer(timers_label, time_remainder):
    minutes, seconds = divmod(time_remainder, 60)
    timers_label.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")


def run_timer(selected_time):
    global remaining_time, timer_running, timer_paused

    remaining_time = selected_time

    while remaining_time > 0:
        if not timer_paused:
            update_timer(timer_label, remaining_time)
            root.update()
            time.sleep(1)
            remaining_time -= 1
        else:
            time.sleep(0.1)

    if timer_running:
        timer_running = False
        play_sound_and_show_message()

    enable_controls(timer_buttons)
    pause_button.config(state="disabled")
    resume_button.config(state="disabled")


def start_timer(selected_time):
    global timer_running, timer_paused

    disable_controls(timer_buttons)
    pause_button.config(state="normal")
    reset_button.config(state="normal")

    timer_running = True
    timer_paused = False

    run_timer(selected_time)

    if timer_running:
        timer_running = False
        play_sound_and_show_message()

    enable_controls(timer_buttons)
    pause_button.config(state="disabled")
    resume_button.config(state="disabled")


def start_timer_thread(selected_time):
    global timer_thread
    if not timer_running:
        timer_thread = threading.Thread(target=start_timer, args=(selected_time,))
        timer_thread.start()


def pause_timer():
    global timer_paused
    pause_button.config(state="disabled")
    resume_button.config(state="normal")
    timer_paused = True


def resume_timer():
    global timer_paused
    resume_button.config(state="disabled")
    pause_button.config(state="normal")
    timer_paused = False
    start_timer_thread(remaining_time)


def reset_timer():
    global remaining_time
    remaining_time = 0
    update_timer(timer_label, remaining_time)
    enable_controls(timer_buttons)
    pause_button.config(state="disabled")
    resume_button.config(state="disabled")


root = tk.Tk()

screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

window_width, window_height = 700, 200
x_position, y_position = (screen_width - window_width) // 2, (
    screen_height - window_height
) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.title("Timer")
root.configure(bg="#EDE7E3")
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "miss_minute.ico")
root.iconbitmap(icon_path)


def create_hover(widget):
    original_bg = widget.cget("bg")

    def on_hover(event):
        widget.config(bg="#edf6f9")

    def on_leave(event):
        widget.config(bg=original_bg)

    widget.bind("<Enter>", on_hover)
    widget.bind("<Leave>", on_leave)


timer_buttons = []


def set_current_timer(timer):
    global current_timer
    current_timer = timer


def on_enter_pressed(event):
    if current_timer == "seven":
        start_timer_7min()
    elif current_timer == "ten":
        start_timer_10min()
    elif current_timer == "fifteen":
        start_timer_15min()

def start_timer_7min():
    set_current_timer("seven")
    start_timer_thread(7 * 60)


def start_timer_10min():
    set_current_timer("ten")
    start_timer_thread(10 * 60)


def start_timer_15min():
    set_current_timer("fifteen")
    start_timer_thread(15 * 60)


def focus_seven(event):
    set_current_timer("seven")


def focus_ten(event):
    set_current_timer("ten")


def focus_fifteen(event):
    set_current_timer("fifteen")

timer_buttons_frame = tk.Frame(root, bg="#EDE7E3")
timer_buttons_frame.pack(side="top", pady=10)

seven_min_button = tk.Button(
    timer_buttons_frame,
    text="7 minutes",
    command=start_timer_7min,
    width=20,
    height=2,
    bg="#FFA62B",
    fg="#0b132b",
)
create_hover(seven_min_button)
seven_min_button.pack(side="left", padx=5)
timer_buttons.append(seven_min_button)

ten_min_button = tk.Button(
    timer_buttons_frame,
    text="10 minutes",
    command=start_timer_10min,
    width=20,
    height=2,
    bg="#FFA62B",
    fg="#0b132b",
)
create_hover(ten_min_button)
ten_min_button.pack(side="left", padx=5)
timer_buttons.append(ten_min_button)

fifteen_min_button = tk.Button(
    timer_buttons_frame,
    text="15 minutes",
    command=start_timer_15min,
    width=20,
    height=2,
    bg="#FFA62B",
    fg="#0b132b",
)
create_hover(fifteen_min_button)
fifteen_min_button.pack(side="left", padx=5)
timer_buttons.append(fifteen_min_button)


pause_button = tk.Button(
    root,
    text="Pause",
    command=pause_timer,
    width=20,
    height=1,
    bg="#1b9ab3",
    fg="#0a0908",
)
create_hover(pause_button)
pause_button.pack()
pause_button.config(state="disabled")

resume_button = tk.Button(
    root,
    text="Resume",
    command=resume_timer,
    width=20,
    height=1,
    bg="#489FB5",
    fg="#0a0908",
)
create_hover(resume_button)
resume_button.pack()
resume_button.config(state="disabled")

reset_button = tk.Button(
    root,
    text="Reset",
    command=reset_timer,
    width=20,
    height=1,
    bg="#82C0CC",
    fg="#0b132b",
)
create_hover(reset_button)
reset_button.pack()
reset_button.config(state="disabled")

timer_label = tk.Label(
    root,
    text="Time Left: ",
    font=("Poppins", 24, "bold"),
    bg="#EDE7E3",
    fg="#0b132b",
)
timer_label.pack()

status_label = tk.Label(
    root,
    text="",
    font=("Poppins", 12),
    bg="#EDE7E3",
    fg="#0b132b",
)
status_label.pack()


seven_min_button.bind("<FocusIn>", focus_seven)
ten_min_button.bind("<FocusIn>", focus_ten)
fifteen_min_button.bind("<FocusIn>", focus_fifteen)

root.bind("<Return>", on_enter_pressed)


root.mainloop()
