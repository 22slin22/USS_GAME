import tkinter as tk
from Axis import *
from Functions import Function
from Utils import *
from tkinter import *


class Graph(tk.Frame):
    # pixels from the left from where the diagram starts
    graph_x_start = 150
    # pixels from the top from where the diagram starts
    graph_y_start = 100

    # x, y points that are drawn for the player curve
    points = []

    def __init__(self, parent, controller, game):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.game = game

        self.function = Function()

        self.canvas_width = self.winfo_screenwidth()
        self.canvas_height = self.winfo_screenheight()

        self.canvas = Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.graph_x_end = self.canvas_width - 100
        self.graph_y_end = self.canvas_height - 150
        self.x_span = self.graph_x_end - self.graph_x_start

    def new_point(self, new_point):
        # calculate x, y position in pixels
        x = self.graph_x_start + (new_point[0] * self.pixels_per_second)
        y = self.graph_y_end - ((new_point[1] - self.game.y_min) * self.pixels_per_cm)

        if len(self.points) > 0:
            self.canvas.create_line(self.points[-1][0], self.points[-1][1], x, y, fill="red", width=3)

        self.points.append([x, y])

    def draw_start_point(self, y):
        x = self.graph_x_start
        y = self.graph_y_end - ((y - self.game.y_min) * self.pixels_per_cm)

        self.canvas.delete('start_point')
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", tags='start_point')

    def reset(self, randomize_function=False, draw_function=True):
        """resets and clears the graph"""
        self.points.clear()

        self.canvas.delete("all")

        self.pixels_per_second = (self.graph_x_end - self.graph_x_start) / self.game.total_time
        self.pixels_per_cm = (self.graph_y_end - self.graph_y_start) / (self.game.y_max - self.game.y_min)
        draw_axis(self.canvas, self.graph_x_start, self.graph_y_start, self.graph_x_end, self.graph_y_end,
                  self.game.y_min, self.game.y_max)
        draw_button_info(self.canvas, "back", "replay", "right")

        if draw_function:
            if randomize_function:
                self.function.randomize_transformation()
            self.function.draw(self.canvas, self.graph_x_start, self.graph_y_start, self.graph_x_end, self.graph_y_end,
                               self.game.interval, width=3, color="black")

    def draw_score(self, score):
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height * 1/8, text="Your score is " + str(score),
                                font=("Times", 70))
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height * 1/4, text="All scores: ",
                                font=("Times", 50))
        for i, score in enumerate(self.game.scores):
            self.canvas.create_text(self.canvas_width / 2, self.canvas_height * 1 / 3 + 50*i,
                                    text=str(i + 1) + ". player " + str(score),
                                    font=("Times", 30))

    def draw_countdown(self, seconds):
        self.canvas.delete("countdown")
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2, text=str(seconds),
                                font=("Times", 80), tags="countdown", fill="darkblue")

    def add_function(self, func):
        self.function.set_scale(self.game.y_min, self.game.y_max, self.game.total_time)
        self.function.set_type(func, rand_transform=True)
        self.function.draw(self.canvas, self.graph_x_start, self.graph_y_start, self.graph_x_end, self.graph_y_end,
                           self.game.interval, width=3, color="black")

    def on_button_pressed(self, button_index):
        if button_index == 0:
            self.game.reset()
            self.controller.show_frame("Functions")
        if button_index == 1:
            self.game.restart()
        if button_index == 2:
            self.game.restart(randomize_function=True)
