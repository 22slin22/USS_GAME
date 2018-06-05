'''
import time
from RPi import GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(7, GPIO.IN)
GPIO.setup(10, False)


def distance():
    GPIO.output(10, True)
    time.sleep(0.00001)
    GPIO.output(10, False)

    start_time = time.monotonic()
    stop_time = time.monotonic()

    while GPIO.input(7) is False:
        start_time = time.monotonic()

    while GPIO.input(7) is True:
        stop_time = time.monotonic()

    distance = ((stop_time - start_time) * 34300) / 2

    return distance
'''

import random
import time


def distance(max_int):
    return random.randint(0, max_int)


def get_velocity(uss, velocity_average, max_int):
    dis = distance(max_int)
    if len(uss) > velocity_average:
        velocity = (dis - uss[-velocity_average][1]) / (time.monotonic() - uss[-velocity_average][0])
        return dis, velocity
    return dis, None
