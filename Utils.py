button_width = 50
button_height = 50

button_delta_y = 90
button_delta_x = 40

button_gap = 20

def draw_button_info(canvas, text0, text1, text2):
    width = canvas.winfo_screenwidth()
    height = canvas.winfo_screenheight()
    
    canvas.create_rectangle(width - button_delta_x - 3*button_width - 2*button_gap, height - button_delta_y - button_height,
                            width - button_delta_x - 2*button_width - 2*button_gap, height - button_delta_y)
    canvas.create_rectangle(width - button_delta_x - 2*button_width - button_gap, height - button_delta_y - button_height,
                            width - button_delta_x - 1*button_width - button_gap, height - button_delta_y)
    canvas.create_rectangle(width - button_delta_x - button_width, height - button_delta_y - button_height,
                            width - button_delta_x, height - button_delta_y)
