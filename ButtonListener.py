# from RPi import GPIO
import time

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(10, GPIO.IN)
# GPIO.setwarnings(False)


class ButtonListener:
    time_click_gap = 0.5
    time_last_click = 0
    state = False

    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame_manager.bind("<Left>", lambda event, button_index=0: self.button_pressed(button_index))
        self.frame_manager.bind("<Down>", lambda event, button_index=1: self.button_pressed(button_index))
        self.frame_manager.bind("<Right>", lambda event, button_index=2: self.button_pressed(button_index))

        # self.frame_manager.frames["StartPage"].bind("")

    def check_buttons(self):
        '''
        if GPIO.input(10) and self.state == False:
            state = True
            if time.monotonic() - self.time_last_click > self.time_click_gap:
                print("clicked")
                self.time_last_click = time.monotonic()
    
        if not GPIO.input(10):
            self.state = False
        '''

    def button_pressed(self, button_index):
        self.frame_manager.on_button_pressed(button_index)
