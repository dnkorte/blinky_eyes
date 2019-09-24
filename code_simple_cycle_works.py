# Skeleton Eyeballs for Cassandra

import board
import time
from digitalio import DigitalInOut, Direction, Pull
import neopixel

# RED = (255, 0, 0, 0)
# YELLOW = (255, 150, 0, 0)
# GREEN = (0, 255, 0, 0)
# CYAN = (0, 255, 255, 0)
# BLUE = (0, 0, 255, 0)
# PURPLE = (180, 0, 255, 0)
# OFF = (0, 0, 0, 0)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
OFF = (0, 0, 0)

# One pixel connected internally!
# dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Digital input with pullup on D7
buttons = []
for p in [board.D7]:
    button = DigitalInOut(p)
    button.direction = Direction.INPUT
    button.pull = Pull.UP
    buttons.append(button)

# NeoPixel strip (of 2 individual LEDS Adafruit 1938) connected on D5
NUMPIXELS = 2
ORDER = neopixel.RGB
neopixels = neopixel.NeoPixel(board.D5, NUMPIXELS, brightness=0.5, auto_write=False, pixel_order=ORDER)

# neopixels = neopixel.NeoPixel(board.D5, NUMPIXELS, brightness=0.2, auto_write=False, pixel_order=(0,1,2,3))

# ######################## MAIN LOOP ##############################

bumpcounter = 0
mode = 0
while True:

    if mode == 0:
        neopixels[0] = RED
        neopixels[1] = RED
    elif mode == 1:
        neopixels[0] = GREEN
        neopixels[1] = GREEN
    elif mode == 2:
        neopixels[0] = BLUE
        neopixels[1] = BLUE
    elif mode == 3:
        neopixels[0] = RED
        neopixels[1] = GREEN
    elif mode == 4:
        neopixels[0] = GREEN
        neopixels[1] = BLUE
    elif mode == 5:
        neopixels[0] = YELLOW
        neopixels[1] = YELLOW
    elif mode == 6:
        neopixels[0] = OFF
        neopixels[1] = OFF
    elif mode == 7:
        neopixels[0] = OFF
        neopixels[1] = OFF
    neopixels.show()

    time.sleep(1)
    mode = mode + 1
    if mode > 7:
        mode = 0