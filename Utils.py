from tkinter import *

button_width = 70
button_height = 70

button_delta_y = 40
button_delta_x = 40

button_gap = 20

imgs = {}


def button_info_init():
    imgs["back"] = PhotoImage(file="Images/Back.png")
    imgs["left"] = PhotoImage(file="Images/Left.png")
    imgs["right"] = PhotoImage(file="Images/Right.png")
    imgs["replay"] = PhotoImage(file="Images/Replay.png")
    imgs["select"] = PhotoImage(file="Images/Select.png")


def draw_button_info(canvas, button_type0, button_type1, button_type2):
    width = canvas.winfo_screenwidth()
    height = canvas.winfo_screenheight()

    xs = [width - button_delta_x - 3*button_width - 2*button_gap,
         width - button_delta_x - 2*button_width - button_gap,
         width - button_delta_x - button_width]

    y = height - button_delta_y - button_height

    # can be left out if button images contain the button outline
    for x in xs:
        canvas.create_rectangle(x, y, x + button_width, y + button_height)

    for i, type in enumerate([button_type0, button_type1, button_type2]):
        """
        y = y
        get the x position with xs[i]
        """
        if type == "back":
            # draw back button
            canvas.create_image(xs[i], y, anchor=NW, image=imgs["back"])
        elif type == "left":
            # draw left button
            canvas.create_image(xs[i], y, anchor=NW, image=imgs["left"])
        elif type == "right":
            # draw right button
            canvas.create_image(xs[i], y, anchor=NW, image=imgs["right"])
        elif type == "replay":
            # draw replay button
            canvas.create_image(xs[i], y, anchor=NW, image=imgs["replay"])
        elif type == "select":
            # draw OK button
            canvas.create_image(xs[i], y, anchor=NW, image=imgs["select"])
