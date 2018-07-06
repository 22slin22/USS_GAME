#from RPi import GPIO
import time

buttons = [11, 13, 15]

"""
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
"""

#for button in buttons:
#    GPIO.setup(button, GPIO.IN)


class ButtonListener:
    time_click_gap = 0.2
    time_last_click = [0, 0, 0]
    state = [False, False, False]

    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame_manager.add_button_listener(self)
        self.frame_manager.bind("<Left>", lambda event, button_index=0: self.button_pressed(button_index))
        self.frame_manager.bind("<Down>", lambda event, button_index=1: self.button_pressed(button_index))
        self.frame_manager.bind("<Right>", lambda event, button_index=2: self.button_pressed(button_index))

    def check_buttons(self):
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
