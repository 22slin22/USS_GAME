from tkinter import *
from Axis import *
from Line import *


class Graph:
    graph_x_start = 100
    graph_y_start = 100

    graph = None

    def __init__(self, game):
        self.tk = Tk()
        self.game = game

        self.pad = 3
        self._geom = '1000x800+0+0'
        self.tk.geometry("{0}x{1}+0+0".format(self.tk.winfo_screenwidth()-self.pad, self.tk.winfo_screenheight()-self.pad))
        self.tk.bind('<Escape>', self.toggle_geom)
        self.tk.bind("<space>", self.restart)
        #   self.tk.overrideredirect(True)

        self.canvas_width = self.tk.winfo_screenwidth()-self.pad
        self.canvas_height = self.tk.winfo_screenheight()-self.pad

        self.canvas = Canvas(self.tk, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.graph_x_end = self.canvas_width - 100
        self.graph_y_end = self.canvas_height - 100
        self.x_span = self.graph_x_end - self.graph_x_start

        self.pixels_per_second = (self.graph_x_end - self.graph_x_start) / game.total_time
        self.pixels_per_cm = (self.graph_y_end - self.graph_y_start) / (game.y_max - game.y_min)

        draw_axis(self.canvas, self.graph_x_start, self.graph_y_start, self.graph_x_end, self.graph_y_end, self.game.y_min, self.game.y_max)

    def new_point(self, new_point):
        x = new_point[0] * self.pixels_per_second
        y = (new_point[1] - self.game.y_min) * self.pixels_per_cm
        draw_new_point(self.canvas, [x, y], self.graph_x_start, self.graph_y_end)

        self.update()

    def draw_start_point(self, y):
        x = self.graph_x_start
        y = (self.graph_y_end - (y * self.pixels_per_cm))

        self.canvas.delete('start_point')
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="orange", tags='start_point')

        self.update()

    def update(self):
        self.tk.update_idletasks()
        self.tk.update()

    def restart(self, event):
        self.reset()
        self.game.restart()

    def reset(self):
        clear_points()

        self.canvas.delete("all")

        draw_axis(self.canvas, self.graph_x_start, self.graph_y_start, self.graph_x_end, self.graph_y_end,
                  self.game.y_min, self.game.y_max)
        draw_graph(self.canvas, self.graph, self.graph_x_start, self.graph_x_end, self.graph_y_start, self.graph_y_end,
                   self.game.total_time, self.game.y_max, self.game.y_min)

    def toggle_geom(self, event):
        geom = self.tk.winfo_geometry()
        self.tk.geometry(self._geom)
        self._geom = geom
        self.tk.overrideredirect(False)

    def draw_score(self, score):
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2, text="Your score is " + str(score),
                                font=("Times", 70))

    def draw_countdown(self, seconds):
        self.canvas.delete("countdown")
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2, text=str(seconds),
                                font=("Times", 80), tags="countdown")

    def add_function(self, func, func_start, func_end, interval):
        self.graph = generate_function_points(func, func_start, func_end, interval, self.game.total_time)
        draw_graph(self.canvas, self.graph, self.graph_x_start, self.graph_x_end, self.graph_y_start, self.graph_y_end,
                   self.game.total_time, self.game.y_max, self.game.y_min)
