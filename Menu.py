import tkinter as tk
from tkinter import font as tkfont


class Menu(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Levels, About):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Levels", command=lambda: controller.show_frame("Levels"))
        button2 = tk.Button(self, text="About", command=lambda: controller.show_frame("About"))
        button1.pack()
        button2.pack()


class Levels(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Levels", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # SPACE FOR LEVELS

        # Sinus
        self.imgSin = tk.PhotoImage(file="WIP.png")
        ButtSin = tk.Button(self, image=self.imgSin).pack()
        # Cosinus
        self.imgCos = tk.PhotoImage(file="WIP.png")
        ButtCos = tk.Button(self, image=self.imgSin).pack()

        # Logarythm
        self.imgLog = tk.PhotoImage(file="WIP.png")
        ButtLog = tk.Button(self, image=self.imgSin).pack()

        # Quadratic
        self.imgQuad = tk.PhotoImage(file="WIP.png")
        ButtQuad = tk.Button(self, image=self.imgSin).pack()

        # GO BACK TO START BUTTON
        self.img0 = tk.PhotoImage(file="Back_Arrow.png")
        button0 = tk.Button(self, text="Go to the start page", image=self.img0, command=lambda: controller.show_frame("StartPage")).pack()


class About(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="About/Help Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # SPACE About


        # GO BACK TO START BUTTON

        self.img0 = tk.PhotoImage(file="Back_Arrow.png")
        button0 = tk.Button(self, text="Go to the start page", image=self.img0, command=lambda: controller.show_frame("StartPage"))
        button0.pack()


if __name__ == "__main__":
    app = Menu()
    app.mainloop()

