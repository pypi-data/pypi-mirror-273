import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageOps

file_path = ""

filters = {
    "Blur": ImageFilter.BLUR,
    "Contour": ImageFilter.CONTOUR,
    "Detail": ImageFilter.DETAIL,
    "Edge Enhance": ImageFilter.EDGE_ENHANCE,
    "Edge Enhance More": ImageFilter.EDGE_ENHANCE_MORE,
    "Emboss": ImageFilter.EMBOSS,
    "Find Edges": ImageFilter.FIND_EDGES,
    "Sharpen": ImageFilter.SHARPEN,
    "Smooth": ImageFilter.SMOOTH,
    "Smooth More": ImageFilter.SMOOTH_MORE,
    "Box Blur": ImageFilter.BoxBlur(10),
    "Gaussian Blur": ImageFilter.GaussianBlur(25),
    "Unsharp Mark": ImageFilter.UnsharpMask,
}


def add_photo():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
    )
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((canvas.winfo_width(), canvas.winfo_height()))
        photo = ImageTk.PhotoImage(img)

        canvas.create_image(
            canvas.winfo_width() / 2,
            canvas.winfo_height() / 2,
            anchor=tk.CENTER,
            image=photo,
        )
        canvas.image = photo


def apply_filter(selected_filter):
    global file_path
    if not file_path:
        return

    image = Image.open(file_path)
    if selected_filter == "Black and White":
        filtered_image = ImageOps.grayscale(image)
    elif selected_filter in filters:
        filter_function = filters[selected_filter]
        if callable(filter_function):
            filtered_image = image.filter(filter_function)
        else:
            filtered_image = image.filter(filter_function)
    else:
        return

    width, height = filtered_image.width, filtered_image.height
    photo = ImageTk.PhotoImage(filtered_image)
    canvas.config(width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.image = photo


def clear_canvas():
    global file_path
    canvas.delete("all")
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((canvas.winfo_width(), canvas.winfo_height()))
        photo = ImageTk.PhotoImage(img)
        canvas.config(width=img.width, height=img.height)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.image = photo


app = tk.Tk()
app.title("Photo Editor")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 1400
window_height = 800
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

left_frame = tk.Frame(app, width=200, height=800, bg="white")
left_frame.pack(side="left", fill="y")

add_btn = tk.Button(left_frame, text="Add photo", width=20, height=1, command=add_photo)
add_btn.pack(pady=15)

canvas = tk.Canvas(app, width=1210, height=800)
canvas.place(x=180, y=-5)

filter_label = tk.Label(left_frame, text="Select Filter", bg="white")
filter_label.pack()
filter_combobox = ttk.Combobox(
    left_frame,
    values=list(filters.keys()),
)
filter_combobox.pack()

clear_button = tk.Button(
    left_frame, text="Clear", width=20, height=1, command=clear_canvas, bg="#FF9797"
)
clear_button.pack(pady=10)

filter_combobox.bind(
    "<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get())
)

app.mainloop()
