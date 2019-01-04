import Menu
import time
import tkinter as tk
from ButtonListener import ButtonListener
from Functions import *
from Graph import Graph
from srf import SRF02

# modes
DISTANCE = 0
VELOCITY = 1

# time it takes until you get back to the menu screen when idling
IDLE_TIME_MENU_SCREEN = 120


class Game:
    mode = 0

    interval = 0.05
    # in seconds
    total_time = 10

    y_max = None
    y_min = None

    # if new point is spike_delta_y away from last point, it wont be drawn
    spike_delta_y = 25
    # number of successive nearby points, after witch they are drawn even if they were not drawn in the first place
    spike_override = 4
    # number of points, that have not been drawn since the last drawn one
    points_not_drawn = 0

    # number of data points that are average to get the position
    average_position = 5
    # number of data points that are average to the velocity
    average_velocity = 20

    # time until the game really starts
    start_up_time = 8
    # idle time between each tick
    waiting_time = 0.01
    show_countdown = True

    # stores every single point measured
    uss = []
    # stores all valid points (points that are not filtered out)
    uss_valid = []
    # stores only points that are drawn
    points = []
    # store the score of all runs with the current graph
    scores = []

    running = False

    def __init__(self):
        self.srf = SRF02()

        self.func = None

        self.frameManager = Menu.FrameManager(self)
        self.button_listener = ButtonListener(self.frameManager)

        self.idle_time = time.monotonic()
        # time of the last action

        self.run()

    def run(self):
        while True:
            if self.running:
                self.tick()
                self.idle_time = time.monotonic()

            self.button_listener.check_buttons()
            self.frameManager.tick()
            time.sleep(self.waiting_time)

            if time.monotonic() - self.idle_time >= IDLE_TIME_MENU_SCREEN and self.frameManager.current_frame_name is not "StartPage":
                self.frameManager.show_frame("StartPage")

    def tick(self):
        if time.monotonic() - self.start_time < self.total_time:
            x, y = self.get_distance()

            if self.filter_point(y):
                self.uss_valid.append([x, y])
                self.points_not_drawn = 0
                if self.mode == DISTANCE:
                    self.add_position_point()
                elif self.mode == VELOCITY:
                    self.add_velocity_point()

            elif self.check_override(y):
                self.add_points_not_drawn()
                self.uss_valid.append([x, y])
                if self.mode == DISTANCE:
                    self.add_position_point()
                elif self.mode == VELOCITY:
                    self.add_velocity_point()

            else:
                self.points_not_drawn += 1
            self.uss.append([x, y])

            if time.monotonic() < self.start_time:
                self.start_point()
            self.countdown()

        else:
            # print(self.uss)
            # print(self.points)
            # print(self.graph.function.shift_x, self.graph.function.shift_y, self.graph.function.squeeze_x, self.graph.function.stretch_y)
            # if the game has ended
            loss = self.calculate_loss()
            self.scores.append(int(1000 / loss))
            print(loss, self.scores[-1])
            self.graph.draw_score(self.scores[-1])
            self.running = False

    def get_distance(self):
        y = self.srf.distance()
        # in Velocity mode y (distance) shouldn't be kept at the velocity_limit (y_max)
        while y < 2 and (self.mode == VELOCITY or y > self.y_max):
            time.sleep(0.05)
            y = self.srf.distance()

        x = time.monotonic() - self.start_time
        return x, y

    def filter_point(self, new_y):
        """tests if the point is not to far from the last point"""
        if len(self.uss_valid) == 0 or math.fabs(new_y - self.uss_valid[-1][1]) < self.spike_delta_y:
            return True
        return False

    def add_points_not_drawn(self):
        """adds the last points that were not drawn"""
        for i in range(self.spike_override - 1):  # -1 because the new point has not been added yet
            x = self.uss[-(self.spike_override - 1 - i)][0]
            y = self.uss[-(self.spike_override - 1 - i)][1]
            self.uss_valid.append([x, y])
        self.points_not_drawn = 0

    def check_override(self, new_y):
        """return True if the the previous 'spike_override' points should be added because they're all in a line"""
        if self.points_not_drawn >= self.spike_override:
            # tests if the newest point lays not on the new line
            if not (math.fabs(new_y - self.uss[-1][1]) < self.spike_delta_y):
                return False
            # tests if the previous points not all lay on one line
            for i in range(self.spike_override - 1):
                if not (math.fabs(self.uss[-i - 1][1] - self.uss[-i - 2][1]) < self.spike_delta_y):
                    return False
            return True
        return False

    def add_position_point(self):
        if len(self.uss_valid) > self.average_position:
            averaged_y = 0
            for n in range(self.average_position):
                averaged_y += self.uss_valid[-n - 1][1]
            averaged_y /= self.average_position
            self.graph.new_point([self.uss_valid[-1][0], averaged_y])
            self.points.append([self.uss_valid[-1][0], averaged_y])

    def add_velocity_point(self):
        if len(self.uss_valid) > self.average_velocity:
            x = self.uss_valid[-1][0]
            v = (self.uss_valid[-1][1] - self.uss_valid[-self.average_velocity][1]) / (
                    x - self.uss_valid[-self.average_velocity][0])
            self.graph.new_point([x, v])
            self.points.append([x, v])

    def start_point(self):
        """when the game hasn't started, draw a point on the y axis"""
        if len(self.points) > 0:
            self.graph.draw_start_point(self.points[-1][1])

    def start(self):
        """Starts a new game"""
        self.frameManager.show_frame("Graph")

        self.graph.reset(draw_function=False)
        self.graph.add_function(self.func)

        self.scores.clear()
        self.start_time = time.monotonic() + self.start_up_time
        self.running = True

    def restart(self, randomize_function=False):
        """restarts the game with the same function"""
        self.reset()
        if randomize_function:
            self.scores.clear()
        self.graph.reset(randomize_function)

        self.start_time = time.monotonic() + self.start_up_time
        self.running = True

    def reset(self):
        """reset the game after each run"""
        self.uss.clear()
        self.points.clear()
        self.show_countdown = True
        self.running = False
        self.points_not_drawn = 0

    def calculate_loss(self):
        """loss is the amount of 'error'"""
        loss = 0
        for point in self.points:
            if 0 <= point[0] <= self.total_time:
                y_ = self.graph.function.evaluate(point[0])
                loss += math.fabs(y_ - point[1])

        # average the loss over all points
        loss = loss / len(self.points)
        return loss

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

    def set_func(self, func):
        self.func = func
        self.frameManager.show_frame("Type")


if __name__ == '__main__':
    game = Game()
