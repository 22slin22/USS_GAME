from Graph import Graph
import Menu
import tkinter as tk
from Functions import *
from srf import SRF02
import time
from ButtonListener import ButtonListener

DISTANCE = 0
VELOCITY = 1


class Game:
    mode = 0
    # number of data points that are average to the velocity
    velocity_average = 4

    # func = "exp"
    # func_start = 0
    # func_end = 5.4

    # func = "log"
    # func_start = 1
    # func_end = 70

    # func = "quad"
    # func_start = -13
    # func_end = 13

    # func = "cos"
    # func = "sin"
    # func_start = 0
    # func_end = 12.6

    interval = 0.05
    total_time = 20

    y_max = 300
    y_min = 0

    # y_max = 500
    # y_min = -500

    # if new point is spike_delta_y away from last point, it wont be drawn
    spike_delta_y = 25
    # number of successive nearby points, after witch they are drawn even if they were not drawn in the first place
    spike_override = 4
    # number of points, that have not been drawn since the last drawn one
    points_not_drawn = 0

    start_up_time = 3
    waiting_time = 0.005
    show_countdown = True

    # stores every single point measured
    uss = []
    # stores only points that are drawn
    points = []

    running = True

    def __init__(self):

        # self.graph = Graph(self)
        self.srf = SRF02()

        # self.start_time = time.monotonic() + self.start_up_time
        # self.run()

        self.func = None
        self.func_start = None
        self.func_end = None

        self.frameManager = Menu.FrameManager(self)
        self.button_listener = ButtonListener(self.frameManager)

        # self.frameManager.mainloop()
        self.frameManager.run()

    def run(self):
        while True:
            while self.running:
                while time.monotonic() - self.start_time < self.total_time:
                    if self.mode == DISTANCE:
                        x, y = self.get_distance()
                        
                        if self.filter_point(y):
                            self.graph.new_point([x, y])
                            self.points.append([x, y])
                            self.points_not_drawn = 0
                        elif self.check_override(y):
                            self.add_points_not_drawn()
                            self.graph.new_point([x, y])
                            self.points.append([x, y])
                        else:
                            self.points_not_drawn += 1
                        self.uss.append([x, y])

                        self.start_point()

                        self.countdown()

                    elif self.mode == VELOCITY:
                        y = self.srf.distance()
                        x = time.monotonic() - self.start_time
                        if self.filter_point(y):
                            self.points.append([x, y])
                            self.points_not_drawn = 0
                            if len(self.points) > self.velocity_average:
                                v = (y - self.points[-self.velocity_average][1]) / (x - self.points[-self.velocity_average][0])
                                self.graph.new_point([x, v])
                                print(v)

                        elif self.check_override(y):
                            self.add_points_not_drawn()
                            self.points.append([x, y])
                            if len(self.points) > self.velocity_average:
                                v = (y - self.points[-self.velocity_average][1]) / (x - self.points[-self.velocity_average][0])
                                self.graph.new_point([x, v])
                                print(v)

                        else:
                            self.points_not_drawn += 1
                        self.uss.append([x, y])

                        self.countdown()

                    time.sleep(self.waiting_time)

                self.running = False
                loss = self.calculate_loss()
                score = int(100000 / loss)
                self.graph.draw_score(score)
                print(loss, score)

            self.graph.update()
            time.sleep(0.2)

    def get_distance(self):
        y = self.srf.distance()
        while y < 5 or y > self.y_max:
            y = self.srf.distance()
            time.sleep(0.04)

        x = time.monotonic() - self.start_time
        return x, y

    def filter_point(self, new_y):
        # tests if the point is not to far from the last point
        if len(self.points) == 0 or math.fabs(new_y - self.points[-1][1]) < self.spike_delta_y:
            return True
        return False

    # adds the last points that were not drawn
    def add_points_not_drawn(self):
        for i in range(self.spike_override-1):          # -1 because the new point has not been added yet
            x = self.uss[-(self.spike_override-1-i)][0]
            y = self.uss[-(self.spike_override-1-i)][1]
            self.graph.new_point([x, y])
            self.points.append([x, y])
        self.points_not_drawn = 0

    # return True if the the last spike_override points should be added because they all lay on one "line"
    def check_override(self, new_y):
        if self.points_not_drawn >= self.spike_override:
            # tests if the newest point lays on the new line
            if not (math.fabs(new_y - self.uss[-1][1]) < self.spike_delta_y):
                return False
            # tests if the last points all lay on one line
            for i in range(self.spike_override - 1):
                if not (math.fabs(self.uss[-i-1][1] - self.uss[-i-2][1]) < self.spike_delta_y):
                    return False
            return True
        return False

    # when the game hasn't started, draw a start point on the y axis
    def start_point(self):
        if time.monotonic() < self.start_time:
            if len(self.points) > 0:
                self.graph.draw_start_point(self.points[-1][1])

    def restart(self):
        self.start_time = time.monotonic() + self.start_up_time
        self.uss.clear()
        self.points.clear()
        self.running = True
        self.show_countdown = True

    def calculate_loss(self):
        loss = 0

        for point in self.points:
            if point[0] > 0:
                y_ = functions(self.func, point[0] / self.total_time * (self.func_end - self.func_start) + self.func_start)
                loss += math.fabs(y_ - point[1])

        loss = loss / len(self.points)
        return loss

    def start(self, func, func_start, func_end):
        self.frameManager.show_frame("Graph")
        self.func = func
        self.func_start = func_start
        self.func_end = func_end

        self.graph.add_function(self.func, self.func_start, self.func_end, self.interval)

        self.restart()
        self.graph.reset()
        self.run()

    def countdown(self):
        if time.monotonic() > self.start_time and self.show_countdown:
            self.show_countdown = False
            self.graph.canvas.delete("countdown")
        if self.show_countdown:
            self.graph.draw_countdown(math.ceil(self.start_time - time.monotonic()))

    def set_mode(self, mode):
        self.mode = mode

    def set_graph(self, graph):
        self.graph = graph

if __name__ == '__main__':
    game = Game()
