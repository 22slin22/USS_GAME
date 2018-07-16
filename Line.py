from Functions import *

points = []


def draw_new_point(canvas, pos, graph_x_start, graph_y_end):
    global points
    x = pos[0] + graph_x_start
    y = graph_y_end - pos[1]

    if len(points) > 0:
        canvas.create_line(points[-1][0], points[-1][1], x, y, fill="red", width=3)

    points.append([x, y])


def generate_function_points(func, func_start, func_end, interval, total_time):
    line = []
    for i in range(int((func_end - func_start) / interval)):
        x = (i*interval) / (func_end - func_start) * total_time
        y = functions(func, func_start + i*interval)
        line.append([x, y])

    return line


def draw_graph(canvas, line, graph_x_start, graph_x_end, graph_y_start, graph_y_end, total_time, y_max, y_min):
    for i, pos in enumerate(line):
        if i == 0:
            continue

        x1 = line[i-1][0]/total_time * (graph_x_end - graph_x_start) + graph_x_start
        y1 = graph_y_end - ((line[i-1][1] - y_min)/(y_max - y_min) * (graph_y_end - graph_y_start))

        x2 = pos[0]/total_time * (graph_x_end - graph_x_start) + graph_x_start
        y2 = graph_y_end - ((pos[1] - y_min)/(y_max - y_min) * (graph_y_end - graph_y_start))

        canvas.create_line(x1, y1, x2, y2, fill="black", width=3)


def clear_points():
    points.clear()
