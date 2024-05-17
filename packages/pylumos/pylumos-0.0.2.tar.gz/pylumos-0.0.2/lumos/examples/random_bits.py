import random
import time

from lumos.lumos import Lumos
from lumos.generator import LumosBitmapGenerator

NUM_LEDS = 72
OFFSET = 4
MAX_BRIGHTNESS = 100

board = Lumos()

board.num_leds(NUM_LEDS)
board.interface.set_power_state(1)

random.seed()

while True:
    idx = random.randint(0, NUM_LEDS - 1)
    r = random.randint(0, MAX_BRIGHTNESS)
    g = random.randint(0, MAX_BRIGHTNESS)
    b = random.randint(0, MAX_BRIGHTNESS)
    board.set_one(idx, r, g, b)
    time.sleep(0.05)