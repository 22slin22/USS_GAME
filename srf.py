# import smbus
import random
import math
import time


class SRF02:
    # def __init__(self):
        # self.i2c = smbus.SMBus(1)
        # self.addr = 0x70

    def distance(self):
        # read the data in inches, so the uss has a bigger range due to not overflowing so fast
        # self.i2c.write_byte_data(self.addr, 0, 80)
        # time.sleep(0.08)
        # dist = self.i2c.read_word_data(self.addr, 2) / 255
        # return dist * 2.54

        return round(random.uniform(50, 250), 2)
