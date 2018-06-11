from Graph import Graph
from Functions import *
from srf import SRF02
import time


class Game:
    velocity = False
    velocity_average = 5

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
    # y_max = 10
    # y_min = -10

    y_max = 300
    y_min = 0

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
        self.graph = Graph(self)
        self.graph.add_function(self.func, self.func_start, self.func_end, self.interval)
        self.srf = SRF02()

        self.start_time = time.monotonic() + self.start_up_time

        self.run()

        self.func = None
        self.func_start = None
        self.func_end = None

    def run(self):
        while True:
            while self.running:
                while time.monotonic() - self.start_time < self.total_time:
                    if self.velocity is False:
                        y = self.srf.distance()
                        self.filter_point(y)

                        if time.monotonic() > self.start_time:
                            self.show_countdown = False
                            self.graph.canvas.delete("countdown")
                        if self.show_countdown:
                            self.graph.draw_countdown(math.ceil(self.start_time - time.monotonic()))

                    '''
                    else:
                        dis, y = get_velocity(self.uss, self.velocity_average)
                        print(y)

                        if len(self.uss) == 0 or math.fabs(dis - self.uss[-1][1]) < self.spike_filtering:
                            self.uss.append([x, dis])
                            if y is not None:
                                self.graph.new_point([x, y])
                                self.points.append([x, y])
                    '''

                    time.sleep(self.waiting_time)

                self.running = False
                loss = self.calculate_loss()
                score = int(100000 / loss)
                self.graph.draw_score(score)
                print(loss, score)

            self.graph.update()
            time.sleep(0.2)

    def filter_point(self, new_y):
        while new_y < 5 or new_y > self.y_max:
            new_y = self.srf.distance()
            time.sleep(0.04)
        new_x = time.monotonic() - self.start_time

        if len(self.points) == 0 \
                or math.fabs(new_y - self.points[-1][1]) < self.spike_delta_y:
            self.graph.new_point([new_x, new_y])
            self.points.append([new_x, new_y])
            self.points_not_drawn = 0
        else:
            if self.check_override(new_y):
                for i in range(self.points_not_drawn):
                    x = self.uss[-(self.points_not_drawn-i)][0]
                    y = self.uss[-(self.points_not_drawn-i)][1]
                    self.graph.new_point([x, y])
                    self.points.append([x, y])
                self.graph.new_point([new_x, new_y])
                self.points.append([new_x, new_y])
                self.points_not_drawn = 0
            else:
                self.points_not_drawn += 1

        self.uss.append([new_x, new_y])

    # return True if the the last spike_override points should be added because they all lay on one "line"
    def check_override(self, new_y):
        if self.points_not_drawn >= self.spike_override:
            if not (math.fabs(new_y - self.uss[-1][1]) < self.spike_delta_y):
                return False
            for i in range(self.spike_override - 1):
                if not (math.fabs(self.uss[-i-1][1] - self.uss[-i-2][1]) < self.spike_delta_y):
                    return False
            return True
        return False

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
                print(point[0])
                y_ = functions(self.func, point[0] / self.total_time * (self.func_end - self.func_start) + self.func_start)
                loss += math.fabs(y_ - point[1])

        loss = loss / len(self.uss)
        return loss

    def set_func(self, func):
        self.func = func

    def set_func_start(self, func_start):
        self.func_start = func_start

    def set_func_end(self, func_end):
        self.func_end = func_end


if __name__ == "__main__":
    Game()
