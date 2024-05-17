from lumos.lumos import Lumos
from lumos.generator import LumosBitmapGenerator

import time

NUM_LEDS = 72
OFFSET = 4

board = Lumos()

board.brightness(10)
board.num_leds(NUM_LEDS)

board.interface.set_power_state(1)

leds = LumosBitmapGenerator(NUM_LEDS)

increment = True
while True:
    for x in range(0 + OFFSET, NUM_LEDS - OFFSET):
        if increment:
            idx = x
        else:
            idx = NUM_LEDS - x - 1
        leds.reset()
        leds.set_pixel(idx, 0, 100, 0)
        leds.set_pixel(idx - 1, 0, 50, 0)
        leds.set_pixel(idx + 1, 0, 50, 0)
        leds.set_pixel(idx - 2, 0, 30, 0)
        leds.set_pixel(idx + 2, 0, 30, 0)
        leds.set_pixel(idx - 3, 0, 15, 0)
        leds.set_pixel(idx + 3, 0, 15, 0)
        leds.set_pixel(idx - 4, 0, 5, 0)
        leds.set_pixel(idx + 4, 0, 5, 0)
        board.interface.send_led_stream(leds.get_byte_stream())
        time.sleep(0.01)
    increment = not increment