def draw_axis(canvas, graph_x_start, graph_y_start, graph_x_end, graph_y_end, y_min, y_max):
    # Draw the 2 main axis
    canvas.create_line(graph_x_start, graph_y_start, graph_x_start, graph_y_end)
    canvas.create_line(graph_x_start, graph_y_start + y_max / (y_max - y_min) * (graph_y_end - graph_y_start),
                       graph_x_end, graph_y_start + y_max / (y_max - y_min) * (graph_y_end - graph_y_start))

    # draw little marks
    for i in range(5):
        canvas.create_line(graph_x_start - 10, graph_y_end - (i + 1) * ((graph_y_end - graph_y_start) / 6),
                           graph_x_start + 10, graph_y_end - (i + 1) * ((graph_y_end - graph_y_start) / 6))

    for i in range(8):
        canvas.create_line(graph_x_start + (i + 1) * ((graph_x_end - graph_x_start) / 9),
                           graph_y_start + y_max / (y_max - y_min) * (graph_y_end - graph_y_start) - 10,
                           graph_x_start + (i + 1) * ((graph_x_end - graph_x_start) / 9),
                           graph_y_start + y_max / (y_max - y_min) * (graph_y_end - graph_y_start) + 10)
