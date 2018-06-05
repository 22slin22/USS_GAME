from Graph import Graph
from Functions import *
from Ultrasonic import *
import time


class Game:
    velocity = False
    velocity_average = 5

    func = "sin"
    func_start = 0
    func_end = 6.3
    interval = 0.05

    start_up_time = 1
    total_time = 20
    y_max = 200
    y_min = 0

    spike_filtering = 30

    uss = []
    points = []

    running = True

    def __init__(self):
        self.graph = Graph(self)
        self.graph.add_function(self.func, self.func_start, self.func_end, self.interval)

        self.start_time = time.monotonic() + self.start_up_time

        self.run()

    def run(self):
        while True:
            while self.running:
                while time.monotonic() < self.start_time:
                    y = distance(self.y_max)
                    self.graph.draw_start_point(y)

                while time.monotonic() - self.start_time < self.total_time:
                    x = time.monotonic() - self.start_time

                    if self.velocity is False:
                        y = distance(self.y_max)
                        if len(self.uss) == 0 or math.fabs(y - self.uss[-1][1]) < self.spike_filtering:
                            self.graph.new_point([x, y])
                            self.uss.append([x, y])
                            self.points.append([x, y])

                    else:
                        dis, y = get_velocity(self.uss, self.velocity_average, self.y_max)

                        if len(self.uss) == 0 or math.fabs(dis - self.uss[-1][1]) < self.spike_filtering:
                            self.uss.append([x, dis])
                            if y is not None:
                                self.graph.new_point([x, y])
                                self.points.append([x, y])

                    time.sleep(0.2)

                self.running = False
                loss = self.calculate_loss()
                score = int(100000 / loss)
                self.graph.draw_score(score)
                print(loss, score)
                # self.graph.tk.mainloop()

            self.graph.update()
            time.sleep(0.2)

    def restart(self):
        self.start_time = time.monotonic() + self.start_up_time
        self.uss.clear()
        self.running = True

    def calculate_loss(self):
        loss = 0

        for point in self.points:
            y_ = functions(self.func, point[0]/self.total_time * (self.func_end - self.func_start) + self.func_start)
            loss += math.fabs(y_ - point[1])

        loss = loss / len(self.points)
        return loss

if __name__ == '__main__':
    Game()
