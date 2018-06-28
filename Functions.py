import math
import random

PADDING = 50


class Function:

    type = None

    shift_x = 0
    shift_y = 0
    squeez_x = 1
    squeez_y = 1

    y_min = 0
    y_max = 0
    y_span = 0

    def set_scale(self, y_min, y_max, total_time):
        self.y_min = y_min
        self.y_max = y_max
        self.y_span = y_max - y_min
        self.total_time = total_time

    def set_type(self, func_type, rand_transform=False):
        self.type = func_type
        if rand_transform:
            if self.type == "lin":
                self.rand_lin_transform()

    def rand_lin_transform(self):
        """x transformations aren't used in linear functions"""
        self.squeez_x = 1
        self.shift_x = 0

        y1 = random.randint(self.y_min+PADDING, self.y_max-PADDING)     # y on the left side
        y2 = random.randint(self.y_min+PADDING, self.y_max-PADDING)     # y on the right side

        self.shift_y = y1       # y - intercept
        self.squeez_y = (y2 - self.shift_y) / self.total_time       # derives from y = mx + t

    def return_function_values(self, interval):
        line = []
        for i in range(int(self.total_time / interval)):
            x = i * interval
            y = self.squeez_y * functions(self.type, self.squeez_x * x - self.shift_x) + self.shift_y
            line.append([x, y])

        return line




def functions(func, x):
    if func == "sin":
        return math.sin(x) * 100 + 150
    elif func == "quad":
        return -1 * math.pow(x, 2) + 250
    elif func == "log":
        return 35 * math.log(x, 2) + 50
    elif func == "exp":
        return math.pow(math.e, x) + 50
    elif func == "lin":
        return x

    else:
        print("Function doesn't exist")
        exit()
