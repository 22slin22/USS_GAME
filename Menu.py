import tkinter as tk
from Functions import Function
from Graph import Graph
from Utils import *
from tkinter import *
from tkinter import font as tkfont


class FrameManager(tk.Tk):
    # Manages the different windows
    current_frame_name = None
    button_listener = None

    def __init__(self, game, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Fullscreen
        self.attributes("-fullscreen", True)
        self.wm_attributes("-topmost", 1)

        # kill program when escape is pressed
        self.bind('<Escape>', lambda event: self.destroy())

        self.game = game

        button_info_init()

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # adds pages to the container
        for F in (StartPage, Type):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        page_name = Functions.__name__
        frame = Functions(parent=container, controller=self, game=self.game)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        page_name = Graph.__name__
        frame = Graph(parent=container, controller=self, game=self.game)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.game.set_graph(self.frames["Graph"])

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        self.current_frame_name = page_name
        frame = self.frames[page_name]
        frame.tkraise()
        frame.focus_set()

    def on_button_pressed(self, button_index):
        self.frames[self.current_frame_name].on_button_pressed(button_index)

    # ticks the windows
    def tick(self):
        self.update_idletasks()
        self.update()

    # adds the button listener to the frames
    def add_button_listener(self, button_listener):
        self.button_listener = button_listener


class StartPage(tk.Frame):
    # Start/Idle Page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=1080, height=720)
        self.controller = controller

        # get screen information for scaling + setting up canvas
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        # Title
        self.canvas.create_text(self.width / 2, self.height / 2, text="Ultra Sonic School Game", fill="darkblue",
                                font="Times 70 italic bold")

        draw_button_info(self.canvas, "select", "select", "select")

    def on_button_pressed(self, button_index):
        self.controller.show_frame("Functions")


class Functions(tk.Frame):
    # Select the function Menu
    selected_button = 0

    def __init__(self, parent, controller, game):
        self.game = game
        tk.Frame.__init__(self, parent)

        # get screen information for scaling + setting up canvas
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.num_buttons = 6

        # +2 to let one button width space on each side
        # +1 because there is one less space between buttons than there are buttons
        # /4 because the space between buttons is 1/4 the button width
        button_width = self.width / ((self.num_buttons + 2) + (self.num_buttons + 1) / 4)
        button_height = button_width
        button_gap = button_width / 4

        self.buttons = []
        function = Function()
        function.set_scale(y_min=0, y_max=1, total_time=1)

        for i in range(self.num_buttons):
            # (button_width*num_buttons + button_gap*(num_buttons-1))/2 to get the left most coordiante
            # i(button_width + button_gap)  to get the current x coordinate
            x1 = self.width / 2 - (button_width * self.num_buttons + button_gap * (self.num_buttons - 1)) / 2 + i * (
                    button_width + button_gap)
            y1 = self.height / 2 - button_height / 2
            x2 = self.width / 2 - (button_width * self.num_buttons + button_gap * (self.num_buttons - 1)) / 2 + (
                    i + 1) * button_width + i * button_gap
            y2 = self.height / 2 + button_height / 2

            self.buttons.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill="white"))

            # sets the right function that is displayed inside the menu
            if i == 0:
                function.set_func_type("lin")
                function.set_transformations(0, 0.25, 1, 0.5)
            elif i == 1:
                function.set_func_type("step")
                function.set_step_transformations(0.25, 3 / 4, 3 / 4)
            elif i == 2:
                function.set_func_type("exp")
                function.set_transformations(0, 0, 5, 0.0234)
            elif i == 3:
                function.set_func_type("log")
                function.set_transformations(-1, 0, 30, 0.221)
            elif i == 4:
                function.set_func_type("quad")
                function.set_transformations(0.5, 0.25, 1, 2)
            elif i == 5:
                function.set_func_type("sin")
                function.set_transformations(0, 0.5, 6.3, 0.3)

            function.draw(self.canvas, x1, y1, x2, y2, interval=0.05, width=2)

        # colour the first button orange
        self.canvas.itemconfig(self.buttons[0], fill="orange")

        function.set_func_type("lin")
        function.set_transformations(0, 0.25, 1, 0.5)

        draw_button_info(self.canvas, "left", "select", "right")

    def on_button_pressed(self, button_index):
        # color current button white -> select new button -> color current button orange -> repeat
        if button_index == 0:
            # go one button left
            self.canvas.itemconfig(self.buttons[self.selected_button], fill="white")
            self.selected_button -= 1
            # goes to rightest button if leftest button is selected
            if self.selected_button < 0:
                self.selected_button = self.num_buttons - 1
            self.canvas.itemconfig(self.buttons[self.selected_button], fill="orange")

        if button_index == 1:
            # sets function when <ok> pressed
            if self.selected_button == 0:
                self.game.set_func("lin")
            elif self.selected_button == 1:
                self.game.set_func("step")
            elif self.selected_button == 2:
                self.game.set_func("exp")
            elif self.selected_button == 3:
                self.game.set_func("log")
            elif self.selected_button == 4:
                self.game.set_func("quad")
            elif self.selected_button == 5:
                self.game.set_func("sin")

        if button_index == 2:
            # go one button right
            self.canvas.itemconfig(self.buttons[self.selected_button], fill="white")
            self.selected_button += 1
            # go to leftest button if last rightest is selected
            if self.selected_button > self.num_buttons - 1:
                self.selected_button = 0

            self.canvas.itemconfig(self.buttons[self.selected_button], fill="orange")


class Type(tk.Frame):

    DISTANCE = 0
    VELOCITY = 1

    # Select whether to play tv or tx
    selected_button = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # get screen information for scaling + setting up canvas
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        # Button dimensions
        button_width = 300
        button_height = 300
        button_gap = 50

        # left button (t/x)
        self.buttons = []
        self.buttons.append(self.canvas.create_rectangle(self.width / 2 - button_gap / 2 - button_width,
                                                         self.height / 2 - button_height / 2,
                                                         self.width / 2 - button_gap / 2,
                                                         self.height / 2 + button_height / 2, fill="orange", tags="0"))
        self.canvas.create_text(self.width / 2 - button_gap / 2 - button_width / 2, self.height / 2, text="t-x",
                                font=("Times", 60))

        # right button (t/v)
        self.buttons.append(
            self.canvas.create_rectangle(self.width / 2 + button_gap / 2, self.height / 2 - button_height / 2,
                                         self.width / 2 + button_gap / 2 + button_width,
                                         self.height / 2 + button_height / 2, tags="1"))
        self.canvas.create_text(self.width / 2 + button_gap / 2 + button_width / 2, self.height / 2, text="t-v",
                                font=("Times", 60))

        draw_button_info(self.canvas, "left", "select", "right")

    def on_button_pressed(self, button_index):
        # color current button white -> select new button -> color current button orange -> repeat
        if button_index == 0:
            # go left
            self.canvas.itemconfig(self.buttons[self.selected_button], fill="white")
            self.selected_button = not self.selected_button
            self.canvas.itemconfig(self.buttons[self.selected_button], fill="orange")
        if button_index == 1:
            # select
            if self.selected_button == 0:
                self.controller.game.y_min = 0
                self.controller.game.y_max = 300
            elif self.selected_button == 1:
                self.controller.game.y_min = -100
                self.controller.game.y_max = 100
            self.controller.game.set_mode(self.selected_button)
            self.controller.game.start()
        if button_index == 2:
            # go right
            self.canvas.itemconfig(self.buttons[self.selected_button], fill="white")
            self.selected_button = not self.selected_button
            self.canvas.itemconfig(self.buttons[self.selected_button], fill="orange")
