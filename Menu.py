import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from Graph import Graph
from Utils import *


class FrameManager(tk.Tk):

    current_frame_name = None
    button_listener = None

    def __init__(self, game, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #self.pad = 3
        self._geom = '1000x800+0+0'
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bind('<Escape>', self.toggle_geom)

        self.game = game

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
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
        '''Show a frame for the given page name'''
        self.current_frame_name = page_name
        frame = self.frames[page_name]
        frame.tkraise()
        frame.focus_set()

    def toggle_geom(self, event):
        geom = self.winfo_geometry()
        self.geometry(self._geom)
        self._geom = geom
        self.overrideredirect(False)

    def on_button_pressed(self, button_index):
        self.frames[self.current_frame_name].on_button_pressed(button_index)

    def run(self):
        while True:
            if self.button_listener is not None:
                self.button_listener.check_buttons()
            self.tick()

    def tick(self):
        self.update_idletasks()
        self.update()

    def add_button_listener(self, button_listener):
        self.button_listener = button_listener


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width= 1080, height=720)
        self.controller = controller
        label = tk.Label(self, text="Ultra Sonic School Game", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Functions", command=lambda: controller.show_frame("Functions")).pack()

    def on_button_pressed(self, button_index):
        self.controller.show_frame("Functions")


class Functions(tk.Frame):

    def __init__(self, parent, controller, game):
        self.game = game
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Funktionstypen", font=controller.title_font)
        label.grid(row=0, column=1)

        # Sinus
        self.imgSin = tk.PhotoImage(file="Sinus.png")
        buttSin = tk.Button(self, image=self.imgSin, command=lambda: self.game.set_func("sin")).grid(row=1, column=0)
        # labelSin = tk.Label(self, text="Trigonometrische").grid(row=2, column=0)

        # Logarythm
        self.imgLog = tk.PhotoImage(file="Log.png")
        buttLog = tk.Button(self, image=self.imgLog, command=lambda: self.game.set_func("log")).grid(row=1, column=1)
        # labelLog = tk.Label(self, text="Logarythmische").grid(row=2, column=0)

        # Quadratic
        self.imgQuad = tk.PhotoImage(file="Quad.png")
        buttQuad = tk.Button(self, image=self.imgQuad, command=lambda: self.game.set_func("quad")).grid(row=1, column=2)
        # labelQuad = tk.Label(self, text="Quadratische").grid(row=2, column=0)
        # Exp
        self.imgExp = tk.PhotoImage(file="Expo.png")
        buttExp = tk.Button(self, image=self.imgExp, command=lambda: self.game.set_func("exp")).grid(row=2, column=0)
        # labelExp = tk.Label(self, text="Exponential").grid(row=2, column=0)

        self.imgLin = tk.PhotoImage(file="Lin.png")
        buttLin = tk.Button(self, image=self.imgLin, command=lambda: self.game.set_func("lin")).grid(row=2, column=1)

        # GO BACK TO START BUTTON
        self.img0 = tk.PhotoImage(file="Back_Arrow.png")
        button0 = tk.Button(self, text="Go back", image=self.img0, command=lambda: controller.show_frame("StartPage")).grid(row=100, column=0)


        #button1 = tk.Button(self, text="Go to the start page", image=img0, command=lambda: controller.show_frame("StartPage")).grid(row=100, column=0)

    def on_button_pressed(self, button_index):
        pass


class Type(tk.Frame):

    selected_button = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="Funtionenart", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)

        # self.img0 = tk.PhotoImage(file="Back_Arrow.png")
        # button0 = tk.Button(self, text="Go to the start page", image=self.img0, command=lambda: controller.show_frame("Functions"))
        # button0.pack()

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        button_width = 300
        button_height = 300
        button_gap = 50
        """left button (t/x)"""
        self.buttons = []
        self.buttons.append(self.canvas.create_rectangle(self.width/2 - button_gap/2 - button_width, self.height/2 - button_height/2,
                                     self.width/2 - button_gap/2, self.height/2 + button_height/2, fill="orange", tags="0"))
        self.canvas.create_text(self.width/2 - button_gap/2 - button_width/2, self.height/2, text="t-x",
                                font=("Times", 60))
        """right button (t/v)"""
        self.buttons.append(self.canvas.create_rectangle(self.width / 2 + button_gap / 2, self.height / 2 - button_height / 2,
                                     self.width / 2 + button_gap / 2 + button_width, self.height / 2 + button_height / 2, tags="1"))
        self.canvas.create_text(self.width / 2 + button_gap / 2 + button_width / 2, self.height / 2, text="t-v",
                                font=("Times", 60))
        draw_button_info(self.canvas, "", "", "")


    #def draw_button(self, index):
    #    if index == 0:


    def on_button_pressed(self, button_index):
        if button_index == 0:
            if self.selected_button > 0:
                self.canvas.itemconfig(self.buttons[self.selected_button], fill="white")
                self.selected_button -= 1
                self.canvas.itemconfig(self.buttons[self.selected_button], fill="orange")
        if button_index == 1:
            if self.selected_button == 0:
                self.controller.game.y_min = 0
                self.controller.game.y_max = 300
            elif self.selected_button == 1:
                self.controller.game.y_min = -100
                self.controller.game.y_max = 100
            self.controller.game.mode = self.selected_button
            self.controller.game.start()

        if button_index == 2:
            if self.selected_button < 1:
                self.canvas.itemconfig(self.buttons[self.selected_button], fill="white")
                self.selected_button += 1
                self.canvas.itemconfig(self.buttons[self.selected_button], fill="orange")
