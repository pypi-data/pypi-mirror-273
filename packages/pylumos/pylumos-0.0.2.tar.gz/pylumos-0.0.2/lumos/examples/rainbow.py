from lumos.lumos import Lumos

import time

board = Lumos()

board.brightness(10)
#board.num_leds(20)

color_steps = 50  # Number of steps between each color transition
colors = [
    (255, 0, 0),    # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (128, 0, 128),  # Violet
]

while True:
    for i in range(len(colors)):  # Iterate through each color transition
        start_color = colors[i]
        end_color = colors[(i + 1) % len(colors)]  # Wrap around to the first color after the last one
        
        # Calculate the incremental change for each color channel
        r_step = (end_color[0] - start_color[0]) / color_steps
        g_step = (end_color[1] - start_color[1]) / color_steps
        b_step = (end_color[2] - start_color[2]) / color_steps
        
        for step in range(color_steps):
            # Calculate the current color based on the step
            current_color = (
                int(start_color[0] + r_step * step),
                int(start_color[1] + g_step * step),
                int(start_color[2] + b_step * step)
            )
            #print(f"RGB: {current_color}")
            board.color(current_color[0], current_color[1], current_color[2])
            time.sleep(0.02)  # Add a small delay for a smoother fading effect