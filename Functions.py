import math
import random


class Function:

    type = None

    shift_x = 0
    shift_y = 0
    squeez_x = 1
    strech_y = 1

    # only for step functions
    m1 = 0
    m2 = 0

    total_time = 0
    y_min = 0
    y_max = 0
    y_span = 0

    def set_scale(self, y_min, y_max, total_time):
        self.y_min = y_min
        self.y_max = y_max
        self.y_span = y_max - y_min
        self.total_time = total_time

        self.min_distance = int(self.y_span / 3)
        # Amount on the graph that is left empty on the bottom and on the top
        self.padding = int(self.y_span / 6)

    def set_type(self, func_type, rand_transform=False):
        self.type = func_type
        if rand_transform:
            self.randomize_transformation()

    def randomize_transformation(self):
        if self.type == "lin":
            self.rand_lin_transform()
        elif self.type == "quad":
            self.rand_quad_transform()
        elif self.type == "sin":
            self.rand_sin_transform()
        elif self.type == "exp":
            self.rand_exp_transform()
        elif self.type == "log":
            self.rand_log_transform()
        elif self.type == "step":
            self.rand_step_transform()

    def rand_lin_transform(self):
        """x transformations aren't used in linear functions"""
        self.squeez_x = 1
        self.shift_x = 0

        y0 = random.randint(self.y_min+self.padding, self.y_max-self.padding)     # y on the left side
        y1 = random.randint(self.y_min+self.padding, self.y_max-self.padding)     # y on the right side
        while math.fabs(y1 - y0) < self.min_distance:
            y0 = random.randint(self.y_min + self.padding, self.y_max - self.padding)  # y on the left side
            y1 = random.randint(self.y_min + self.padding, self.y_max - self.padding)  # y on the right side

        self.shift_y = y0       # y - intercept
        self.strech_y = (y1 - self.shift_y) / self.total_time       # derives from y = mx + t

    def rand_quad_transform(self):
        self.squeez_x = 1       # not used in quadratic functions
        self.shift_x = self.total_time / 2

        xv = self.total_time / 2                                        # x coordinate of the vertex is in the middle
        yv = random.randint(self.y_min+self.padding, self.y_max-self.padding)     # y coordinate of the vertex
        y0 = random.randint(self.y_min+self.padding, self.y_max-self.padding)     # y on the left side (also on the right side)
        while math.fabs(yv - y0) < self.min_distance:
            yv = random.randint(self.y_min + self.padding, self.y_max - self.padding)  # y on the left side
            y0 = random.randint(self.y_min + self.padding, self.y_max - self.padding)  # y on the right side

        self.strech_y = (y0 - yv) / math.pow(xv, 2)                     # derives from y = a(x-xv)² + yv
        self.shift_y = yv

    def rand_sin_transform(self):
        self.strech_y = random.randint(self.min_distance / 2, self.y_span / 2 - self.padding)
        while math.fabs(self.strech_y*2) < self.min_distance:
            self.strech_y = random.randint(self.min_distance/2, self.y_span/2 - self.padding)

        self.shift_x = random.randint(0, self.total_time)      # shift any amount (sin is cyclic)
        self.shift_y = (self.y_min + self.y_max) / 2                      # in the middle

        periods = 2 * random.random() + 2                       # 1-2 periods
        self.squeez_x = periods * math.pi / self.total_time     # scaled to the scale   sin(2*pi*x) -> one period prom 0 to 1

    def rand_exp_transform(self):
        self.shift_x = 0
        self.shift_y = self.y_min + self.padding      # not random to get a reasonable graph

        self.squeez_x = random.random()     # so small to fit the plot on the graph
        self.strech_y = random.random()

        y_right = self.evaluate(self.total_time)
        while not (self.y_min + self.padding < int(y_right) < self.y_max - self.padding and y_right - self.shift_y > self.min_distance):
            self.squeez_x = random.random()
            self.strech_y = random.random()
            y_right = self.evaluate(self.total_time)

    def rand_log_transform(self):
        self.shift_x = -1       # so no infinite values
        self.shift_y = self.y_min + self.padding     # to fit graph

        self.strech_y = random.randint(1, 100)
        self.squeez_x = random.randint(1, 15)

        y_right = self.evaluate(self.total_time)
        while not (self.y_min + self.padding < int(y_right) < self.y_max - self.padding and y_right - self.shift_y > self.min_distance):
            self.strech_y = random.randint(1, 100)
            self.squeez_x = random.randint(1, 15)
            y_right = self.evaluate(self.total_time)

    def rand_step_transform(self):
        self.shift_x = random.randint(self.y_min+self.padding, self.y_max-self.padding)
        y_middle = random.randint(self.y_min+self.padding, self.y_max-self.padding)
        y_right = random.randint(self.y_min+self.padding, self.y_max-self.padding)
        while math.fabs(y_middle - self.shift_x) < self.min_distance:
            y_middle = random.randint(self.y_min + self.padding, self.y_max - self.padding)
        while math.fabs(y_right - y_middle) < self.min_distance:
            y_right = random.randint(self.y_min + self.padding, self.y_max - self.padding)

        self.m1 = (y_middle - self.shift_x) / (self.total_time / 3)
        self.m2 = (y_right - y_middle) / (self.total_time / 3)

    def evaluate(self, x):
        if self.type == "step":
            if x < self.total_time/3:
                return self.m1 * x + self.shift_x
            elif x < self.total_time * 2/3:
                return self.m1 * (self.total_time/3) + self.shift_x
            else:
                return (self.m1 * (self.total_time/3) + self.shift_x) + (self.m2 * (x - self.total_time * 2/3))
        # with any other function
        else:
            return self.strech_y * functions(self.type, self.squeez_x * x - self.shift_x) + self.shift_y

    def return_function_values(self, interval):
        line = []
        for i in range(int(self.total_time / interval) + 1):
            x = i * interval
            y = self.evaluate(x)
            line.append([x, y])

        return line

    def set_transformations(self, shift_x, shift_y, squeez_x, strech_y):
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.squeez_x = squeez_x
        self.strech_y = strech_y

    def set_step_transformations(self, shift_x, m1, m2):
        self.shift_x = shift_x
        self.m1 = m1
        self.m2 = m2

    def draw(self, canvas, graph_x_start, graph_y_start, graph_x_end, graph_y_end, interval, width=5):
        line = self.return_function_values(interval)
        for i, pos in enumerate(line):
            if i == 0:
                continue

            x1 = line[i-1][0]/self.total_time * (graph_x_end - graph_x_start) + graph_x_start
            y1 = graph_y_end - ((line[i-1][1] - self.y_min)/(self.y_max - self.y_min) * (graph_y_end - graph_y_start))

            x2 = pos[0]/self.total_time * (graph_x_end - graph_x_start) + graph_x_start
            y2 = graph_y_end - ((pos[1] - self.y_min)/(self.y_max - self.y_min) * (graph_y_end - graph_y_start))

            canvas.create_line(x1, y1, x2, y2, fill="grey", width=width)




def functions(func, x):
    if func == "sin":
        return math.sin(x)
    elif func == "quad":
        return math.pow(x, 2)
    elif func == "log":
        return math.log(x, math.e)
    elif func == "exp":
        return math.pow(2, x)
    elif func == "lin":
        return x

    else:
        print("Function doesn't exist")
        exit()
