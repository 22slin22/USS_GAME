import math


def functions(func, x):
    if func == "sin":
        return math.sin(x) * 100 + 150
    if func == "cos":
        return math.cos(x) * 100 + 150
    if func == "quad":
        return -1 * math.pow(x, 2) + 250
    if func == "log":
        return 35 * math.log(x, 2) + 50
    if func == "exp":
        return math.pow(math.e, x) + 50

    else:
        print("Function doesn't exist")
        exit()
