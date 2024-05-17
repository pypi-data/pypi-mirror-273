
DEFAULT_LED_STRING_LENGTH = 16

class LumosBit():

    def __init__(self, R, G, B):
        self.data = {
            "R": R,
            "G": G,
            "B": B,
        }
    
    

class LumosBitmapGenerator():

    pixel_data = bytearray()

    def __init__(self, num_leds=DEFAULT_LED_STRING_LENGTH):
        self.num_leds = num_leds
        self.pixel_data = bytearray(4 * self.num_leds)
    
    def reset(self):
        self.pixel_data = bytearray(4 * self.num_leds)
    
    def set_pixel(self, pixel_idx, r, g, b):
        self.pixel_data[4 * pixel_idx + 0] = b
        self.pixel_data[4 * pixel_idx + 1] = r
        self.pixel_data[4 * pixel_idx + 2] = g
    
    def get_byte_stream(self):
        return self.pixel_data
