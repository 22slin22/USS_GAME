# from RPi import GPIO
import time

# GPIO Ports
buttons = [11, 12, 13]


# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)


# for button in buttons:
#    GPIO.setup(button, GPIO.IN)


class ButtonListener:
    # time before the next button press is registered
    time_click_gap = 0.2
    time_last_click = [0, 0, 0]
    # button states (not pressed | pressed)
    state = [False, False, False]

    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame_manager.add_button_listener(self)
        # binding the buttons to keys for debugging purposes
        self.frame_manager.bind("<Left>", lambda event, button_index=0: self.button_pressed(button_index))
        self.frame_manager.bind("<Down>", lambda event, button_index=1: self.button_pressed(button_index))
        self.frame_manager.bind("<Right>", lambda event, button_index=2: self.button_pressed(button_index))

    def check_buttons(self):
        """check if a button is pressed"""
        """
        for i, button in enumerate(buttons):
            if GPIO.input(button) and self.state[i] == False:
                self.state[i] = True
                if time.monotonic() - self.time_last_click[i] > self.time_click_gap:
                    self.button_pressed(i)
                    self.time_last_click[i] = time.monotonic()
        
            if not GPIO.input(button):
                self.state[i] = False
        """
        pass

    def button_pressed(self, button_index):
        self.frame_manager.on_button_pressed(button_index)
        self.frame_manager.game.idle_time = time.monotonic()
