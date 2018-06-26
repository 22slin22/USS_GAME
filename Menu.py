import tkinter as tk
from tkinter import font as tkfont
from Graph import Graph


class FrameManager(tk.Tk):

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
        frame = self.frames[page_name]
        frame.tkraise()
        frame.focus_set()

    def toggle_geom(self, event):
        geom = self.winfo_geometry()
        self.geometry(self._geom)
        self._geom = geom
        self.overrideredirect(False)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width= 1080, height=720)
        self.controller = controller
        label = tk.Label(self, text="Ultra Sonic School Game", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Functions", command=lambda: controller.show_frame("Functions")).pack()


class Functions(tk.Frame):

    def __init__(self, parent, controller, game):
        self.game = game
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Funktionen Typen", font=controller.title_font)
        label.grid(row=0, column=2)

        # SPACE FOR LEVELS

        # Sinus
        self.imgSin = tk.PhotoImage(file="Sinus.png")
        buttSin = tk.Button(self, image=self.imgSin, command=lambda: self.game.start("sin", 0, 12.6)).grid(row=1, column=0)
        # labelSin = tk.Label(self, text="Trigonometrische").grid(row=2, column=0)

        # Logarythm
        self.imgLog = tk.PhotoImage(file="Log.png")
        buttLog = tk.Button(self, image=self.imgLog, command=lambda: self.game.start("log", 1, 70)).grid(row=1, column=1)
        # labelLog = tk.Label(self, text="Logarythmische").grid(row=2, column=0)

        # Quadratic
        self.imgQuad = tk.PhotoImage(file="Quad.png")
        buttQuad = tk.Button(self, image=self.imgQuad, command=lambda: self.game.start("quad", -13, 13)).grid(row=1, column=2)
        # labelQuad = tk.Label(self, text="Quadratische").grid(row=2, column=0)
        # Exp
        self.imgExp = tk.PhotoImage(file="Expo.png")
        buttQuad = tk.Button(self, image=self.imgExp, command=lambda: self.game.start("exp", 0, 5.4)).grid(row=1, column=3)
        # labelExp = tk.Label(self, text="Exponential").grid(row=2, column=0)

        # GO BACK TO START BUTTON
        self.img0 = tk.PhotoImage(file="Back_Arrow.png")
        button0 = tk.Button(self, text="Go back", image=self.img0, command=lambda: controller.show_frame("StartPage")).grid(row=100, column=0)


        #button1 = tk.Button(self, text="Go to the start page", image=img0, command=lambda: controller.show_frame("StartPage")).grid(row=100, column=0)


class Type(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="About/Help Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.img0 = tk.PhotoImage(file="Back_Arrow.png")
        button0 = tk.Button(self, text="Go to the start page", image=self.img0, command=lambda: controller.show_frame("Functions"))
        button0.pack()
