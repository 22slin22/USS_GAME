import math


def functions(func, x):
    if func == "sin":
        return math.sin(x) * 100 + 150
    else:
        print("Function doesn't exist")
        exit()
