def disable_controls(timer_buttons):
    for button in timer_buttons:
        button.config(state="disabled")


def enable_controls(timer_buttons):
    for button in timer_buttons:
        button.config(state="normal")
