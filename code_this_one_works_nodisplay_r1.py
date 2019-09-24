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
ORANGE = (80, 40, 0)
OFF = (0, 0, 0)

mode = 0
mode_initiated = False
mode_duration_counter = 0
mode_phase = 0
HIGHEST_MODE = 8

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Digital input with pullup on D7
button = DigitalInOut(board.D7)
button.direction = Direction.INPUT
button.pull = Pull.UP

# NeoPixel strip (of 2 individual LEDS Adafruit 1938) connected on D5
NUMPIXELS = 2
ORDER = neopixel.RGB
neopixels = neopixel.NeoPixel(board.D5, NUMPIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)

######################### HELPERS ##############################

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos*3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos*3), 0, int(pos*3)]
    else:
        pos -= 170
        return [0, int(pos*3), int(255 - pos*3)]


# ######################## MAIN LOOP ##############################


while True:
    # check_button()
    if not button.value:
        led.value = True
        mode = mode + 1
        if mode > HIGHEST_MODE:
            mode = 0
        mode_initiated = False
        mode_duration_counter = 0
        mode_phase = 0
        while not button.value:
            pass
        led.value = False

    if mode_initiated:
        mode_duration_counter = mode_duration_counter + 1

    if mode == 0:                   # both solid red
        if not mode_initiated:
            neopixels[0] = RED
            neopixels[1] = RED
            neopixels.show()
            mode_initiated = True

    elif mode == 1:                 # both solid green
        if not mode_initiated:
            neopixels[0] = GREEN
            neopixels[1] = GREEN
            neopixels.show()
            mode_initiated = True

    elif mode == 2:                 # both solid blue
        if not mode_initiated:
            neopixels[0] = BLUE
            neopixels[1] = BLUE
            neopixels.show()
            mode_initiated = True

    elif mode == 3:                 # both solid yellow
        if not mode_initiated:
            neopixels[0] = YELLOW
            neopixels[1] = YELLOW
            neopixels.show()
            mode_initiated = True

    elif mode == 4:                 # flipping red / green
        if not mode_initiated:
            neopixels[0] = RED
            neopixels[1] = GREEN
            mode_phase = 1          # for this mode phase 0 is R/G, phase 1 is G/R
            neopixels.show()
            mode_initiated = True
        else:
            if mode_duration_counter >= 9:
                if mode_phase == 0:
                    neopixels[0] = GREEN
                    neopixels[1] = RED
                    mode_phase = 1
                else:
                    neopixels[0] = RED
                    neopixels[1] = GREEN
                    mode_phase = 0
                neopixels.show()
                mode_duration_counter = 0

    elif mode == 5:                 # flashing yellow
        if not mode_initiated:
            neopixels[0] = YELLOW
            neopixels[1] = YELLOW
            mode_phase = 1          # for this mode phase 0 is R/G, phase 1 is G/R
            neopixels.show()
            mode_initiated = True
        else:
            if mode_duration_counter >= 5:
                if mode_phase == 0:
                    neopixels[0] = OFF
                    neopixels[1] = OFF
                    mode_phase = 1
                else:
                    neopixels[0] = YELLOW
                    neopixels[1] = YELLOW
                    mode_phase = 0
                neopixels.show()
                mode_duration_counter = 0
            mode_initiated = True

    elif mode == 6:                 # flipping blue / yellow
        if not mode_initiated:
            neopixels[0] = YELLOW
            neopixels[1] = BLUE
            mode_phase = 1          # for this mode phase 0 is R/G, phase 1 is G/R
            neopixels.show()
            mode_initiated = True
        else:
            if mode_duration_counter >= 9:
                if mode_phase == 0:
                    neopixels[0] = BLUE
                    neopixels[1] = YELLOW
                    mode_phase = 1
                else:
                    neopixels[0] = YELLOW
                    neopixels[1] = BLUE
                    mode_phase = 0
                neopixels.show()
                mode_duration_counter = 0


    elif mode == 7:                 # rainbow effect
        if not mode_initiated:
            mode_initiated = True
            mode_duration_counter = 32      # just so it starts in the middle

        # then this speeds it up a bit
        if mode_duration_counter > 84:
            mode_duration_counter = 0
        baseCode = mode_duration_counter * 3

        neopixels[0] = wheel(baseCode)
        neopixels[1] = wheel(255 - baseCode)
        neopixels.show()

    elif mode == 8:                 # fast flipping red / green
        if not mode_initiated:
            neopixels[0] = RED
            neopixels[1] = GREEN
            mode_phase = 1          # for this mode phase 0 is R/G, phase 1 is G/R
            neopixels.show()
            mode_initiated = True
        else:
            if mode_duration_counter >= 3:
                if mode_phase == 0:
                    neopixels[0] = GREEN
                    neopixels[1] = RED
                    mode_phase = 1
                else:
                    neopixels[0] = RED
                    neopixels[1] = GREEN
                    mode_phase = 0
                neopixels.show()
                mode_duration_counter = 0

    time.sleep(0.1)