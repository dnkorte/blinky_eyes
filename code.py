# blinky eyeballs for classroom skull; this version uses TFT display
# 
# MIT License
# 
# Copyright (c) 2019 Don Korte
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

"""
blinky eyeballs for classroom skull; CircuitPython version 
===========================================================

Author(s):  Don Korte
Repository: https://github.com/dnkorte/blinky_eyes

this version uses TFT display, and requires an M4 class ItsyBitsy
must create lib/ folder and install the following Adafruit libraries:
    adafruit_display_text (folder)
    adafruit_display_shapes (folder)
    adafruit_st7735r.mpy
    adafruit_debouncer.mpy
    neopixel.mpy

ItsyBitsy pin connections:
    to NeoPixel: 5!
    to TFT (1.8in TFT http://www.adafruit.com/products/358):
        SCK /   SCK
        MOSI /  MOSI
        10:     CS
        9:      Reset
        7:      DC
        (Note also TFT requires power, ground, and backlight)
        (Note also ItsyBitsy requires Vbat and Gnd, and it also supplies power for PB pullup (Vhi))
    to pushbutton: 11  (normally pulled high, press takes it low)
"""

import board
import time
from digitalio import DigitalInOut, Direction, Pull
import displayio
import terminalio
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
from adafruit_debouncer import Debouncer
import neopixel

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def display_line1(text):
    line1_textbox.text = text
    _, _, textwidth, _ = line1_textbox.bounding_box
    # note this field is scaled by 2 so we initially center it in a 80 pixel space
    new_x = int(2 * (40 - (textwidth/2)))
    text_group1.x = new_x

def display_line2(text):
    line2_textbox.text = text
    _, _, textwidth, _ = line2_textbox.bounding_box
    # note this field is scaled by 2 so we initially center it in a 80 pixel space
    new_x = int(2 * (40 - (textwidth/2)))
    text_group2.x = new_x

def display_line3(text):
    modenum_textbox.text = text
    _, _, textwidth, _ = modenum_textbox.bounding_box
    # note this field is scaled by 3 so we initially center it in a 53 pixel space
    new_x = int(3 * (26.5 - (textwidth/2)))
    text_group3.x = new_x

# setup for NeoPixels (RGB) ########################################################
# NeoPixel "strip" (of 2 individual LEDS Adafruit 1938) connected on D5

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
UGLYORANGE = (80, 40, 0)
ORANGE1 = (115, 20, 0)
ORANGE = (115, 25, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTGRAY = (100, 100, 100)
OFF = (0, 0, 0)

NUMPIXELS = 2
ORDER = neopixel.RGB
neopixels = neopixel.NeoPixel(board.D5, NUMPIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)

# color definitions for TFT display
D_RED = 0xFF0000
D_GREEN = 0x00FF00
D_BLUE = 0x0000FF
D_YELLOW = 0xFFFF00
D_ORANGE = 0xFF8000
D_BLACK = 0x000000
D_WHITE = 0xFFFFFF

# setup ST7735 display 1.8in TFT http://www.adafruit.com/products/358 ###############
# see https://github.com/adafruit/Adafruit_CircuitPython_ST7735R/blob/master/examples/st7735r_128x160_simpletest.py
spi = board.SPI()
tft_cs = board.D10
tft_dc = board.D7

displayio.release_displays()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)

display = ST7735R(display_bus, width=160, height=128, rotation=90, bgr=True)

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

left_circle = Circle(40, 30, 15, fill=D_RED)
splash.append(left_circle)
right_circle = Circle(120, 30, 15, fill=D_RED)
splash.append(right_circle)

text = ""
text_group1 = displayio.Group(max_size=2, scale=2, x=0, y=88)
line1_textbox = label.Label(terminalio.FONT, text=text, color=D_YELLOW, max_glyphs=12)
text_group1.append(line1_textbox) 
splash.append(text_group1)

text_group2 = displayio.Group(max_size=2, scale=2, x=0, y=112)
line2_textbox = label.Label(terminalio.FONT, text=text, color=D_YELLOW, max_glyphs=12)
text_group2.append(line2_textbox) 
splash.append(text_group2)

# text_group3 = displayio.Group(max_size=2, scale=3, x=72, y=56)
text_group3 = displayio.Group(max_size=2, scale=3, x=0, y=56)
modenum_textbox = label.Label(terminalio.FONT, text=text, color=D_YELLOW, max_glyphs=2)
text_group3.append(modenum_textbox) 
splash.append(text_group3)


# setup environment #################################################################
mode = 0
mode_initiated = False
mode_duration_counter = 0
mode_phase = 0
HIGHEST_MODE = 10
icon_counter = 0
fastloop_counter = 0

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Digital input with pullup on D7
button = DigitalInOut(board.D11)
button.direction = Direction.INPUT
button.pull = Pull.UP
debounced_button = Debouncer(button)


left_colors = [ D_RED, D_RED, D_RED, D_RED, D_RED, D_RED, D_RED, D_RED ]
right_colors = [ D_RED, D_RED, D_RED, D_RED, D_RED, D_RED, D_RED, D_RED ]

while True:
    # check_button()
    debounced_button.update()
    if debounced_button.fell:
        mode += 1
        if mode > HIGHEST_MODE:
            mode = 0
        mode_initiated = False
        mode_duration_counter = 0
        mode_phase = 0

    time.sleep(0.01)
    fastloop_counter += 1
    if fastloop_counter > 9:
        fastloop_counter = 0
    else:
        continue

    led.value = not debounced_button.value

    if mode_initiated:
        mode_duration_counter = mode_duration_counter + 1

    icon_counter += 1
    if icon_counter > 7:
        icon_counter = 0
    left_circle.fill = left_colors[icon_counter]
    right_circle.fill = right_colors[icon_counter]

    if mode == 0:                   # both solid red
        if not mode_initiated:
            mode_initiated = True
            display_line1("RED RED")
            display_line2("SOLID")
            display_line3(str(mode))
            left_colors = [ D_RED, D_RED, D_RED, D_RED, D_RED, D_RED, D_RED, D_RED ]
            right_colors = [ D_RED, D_RED, D_RED, D_RED, D_RED, D_RED, D_RED, D_RED ]
            neopixels[0] = RED
            neopixels[1] = RED
            neopixels.show()

    elif mode == 1:                 # both solid green
        if not mode_initiated:
            mode_initiated = True
            display_line1("GREEN GREEN")
            display_line2("SOLID")
            display_line3(str(mode))
            left_colors = [ D_GREEN, D_GREEN, D_GREEN, D_GREEN, D_GREEN, D_GREEN, D_GREEN, D_GREEN ]
            right_colors = [ D_GREEN, D_GREEN, D_GREEN, D_GREEN, D_GREEN, D_GREEN, D_GREEN, D_GREEN ]
            neopixels[0] = GREEN
            neopixels[1] = GREEN
            neopixels.show()

    elif mode == 2:                 # both solid blue
        if not mode_initiated:
            mode_initiated = True
            display_line1("BLUE BLUE")
            display_line2("SOLID")
            display_line3(str(mode))
            left_colors = [ D_BLUE, D_BLUE, D_BLUE, D_BLUE, D_BLUE, D_BLUE, D_BLUE, D_BLUE ]
            right_colors = [ D_BLUE, D_BLUE, D_BLUE, D_BLUE, D_BLUE, D_BLUE, D_BLUE, D_BLUE ]
            neopixels[0] = BLUE
            neopixels[1] = BLUE
            neopixels.show()

    elif mode == 3:                 # both solid yellow
        if not mode_initiated:
            mode_initiated = True
            display_line1("YELLO YELLO")
            display_line2("SOLID")
            display_line3(str(mode))
            left_colors = [ D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW ]
            right_colors = [ D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW ]
            neopixels[0] = YELLOW
            neopixels[1] = YELLOW
            neopixels.show()

    elif mode == 4:                 # flipping red / green
        if not mode_initiated:
            mode_initiated = True
            mode_phase = 0
            mode_duration_counter = 99          # force it to rewrite LEDs at first loop
            display_line1("RED GREEN")
            display_line2("FLIP")
            display_line3(str(mode))
            left_colors = [ D_RED, D_RED, D_GREEN, D_GREEN, D_RED, D_RED, D_GREEN, D_GREEN ]
            right_colors = [ D_GREEN, D_GREEN, D_RED, D_RED, D_GREEN, D_GREEN, D_RED, D_RED ]
        else:
            if mode_duration_counter >= 12:
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
            mode_initiated = True
            mode_phase = 0
            mode_duration_counter = 99          # force it to rewrite LEDs at first loop
            display_line1("YELLO YELLO")
            display_line2("FLASH")
            display_line3(str(mode))
            left_colors = [ D_YELLOW, D_YELLOW, D_BLACK, D_BLACK, D_YELLOW, D_YELLOW, D_BLACK, D_BLACK ]
            right_colors = [ D_YELLOW, D_YELLOW, D_BLACK, D_BLACK, D_YELLOW, D_YELLOW, D_BLACK, D_BLACK ]
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

    elif mode == 6:                 # flipping blue / yellow
        if not mode_initiated:
            mode_initiated = True
            mode_phase = 0
            mode_duration_counter = 99          # force it to rewrite LEDs at first loop
            display_line1("BLUE YELLOW")
            display_line2("FLIP")
            display_line3(str(mode))
            left_colors = [ D_BLUE, D_BLUE, D_YELLOW, D_YELLOW, D_BLUE, D_BLUE, D_YELLOW, D_YELLOW ]
            right_colors = [ D_YELLOW, D_YELLOW, D_BLUE, D_BLUE, D_YELLOW, D_YELLOW, D_BLUE, D_BLUE ]
        else:
            if mode_duration_counter >= 12:
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

    elif mode == 7:                 # flipping orange / yellow
        if not mode_initiated:
            mode_initiated = True
            mode_phase = 0
            mode_duration_counter = 99          # force it to rewrite LEDs at first loop
            display_line1("ORANG YELLO")
            display_line2("FLIP")
            display_line3(str(mode))
            left_colors = [ D_ORANGE, D_ORANGE, D_YELLOW, D_YELLOW, D_ORANGE, D_ORANGE, D_YELLOW, D_YELLOW ]
            right_colors = [ D_YELLOW, D_YELLOW, D_ORANGE, D_ORANGE, D_YELLOW, D_YELLOW, D_ORANGE, D_ORANGE ]
        else:
            if mode_duration_counter >= 12:
                if mode_phase == 0:
                    neopixels[0] = ORANGE
                    neopixels[1] = YELLOW
                    mode_phase = 1
                else:
                    neopixels[0] = YELLOW
                    neopixels[1] = ORANGE
                    mode_phase = 0
                neopixels.show()
                mode_duration_counter = 0

    elif mode == 8:                 # pulsing orange and white for pumpkin eyes
        if not mode_initiated:
            mode_initiated = True
            mode_duration_counter = 99          # force it to rewrite LEDs at first loop
            display_line1("PUMPKIN")
            display_line2(" ")
            display_line3(str(mode))
            left_colors = [ D_ORANGE, D_ORANGE, D_ORANGE, D_ORANGE, D_ORANGE, D_ORANGE, D_ORANGE, D_WHITE ]
            right_colors = [ D_ORANGE, D_ORANGE, D_ORANGE, D_ORANGE, D_ORANGE, D_ORANGE, D_ORANGE, D_WHITE ]
        else:
            if mode_duration_counter == 45:
                neopixels[0] = WHITE
                neopixels[1] = WHITE
                neopixels.show()
            elif mode_duration_counter == 47:
                neopixels[0] = ORANGE
                neopixels[1] = ORANGE
                neopixels.show()
            elif mode_duration_counter == 48:
                neopixels[0] = WHITE
                neopixels[1] = WHITE
                neopixels.show()
            if mode_duration_counter > 49:
                neopixels[0] = ORANGE
                neopixels[1] = ORANGE
                neopixels.show()
                mode_duration_counter = 0


    elif mode == 9:                 # fast flipping red / green
        if not mode_initiated:
            mode_initiated = True
            mode_phase = 0
            mode_duration_counter = 99          # force it to rewrite LEDs at first loop
            display_line1("RED GREEN")
            display_line2("FAST FLIP")
            display_line3(str(mode))
            left_colors = [ D_RED, D_GREEN, D_RED, D_GREEN, D_RED, D_GREEN, D_RED, D_GREEN ]
            right_colors = [ D_GREEN, D_RED, D_GREEN, D_RED , D_GREEN, D_RED, D_GREEN, D_RED ]
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


    elif mode == 10:                 
        if not mode_initiated:
            mode_phase = 1
            mode_initiated = True
            display_line1("RAINBOW")
            display_line2(" ")
            display_line3(str(mode))
            left_colors = [ D_RED, D_RED, D_RED, D_ORANGE, D_ORANGE, D_ORANGE, D_YELLOW, D_YELLOW ]
            right_colors = [ D_YELLOW, D_YELLOW, D_GREEN, D_GREEN, D_GREEN, D_BLUE, D_BLUE, D_BLUE ]
        else:
            mode_phase += 3
            if mode_phase > 255:
                mode_phase = 1
            neopixels[0] = wheel(mode_phase)
            neopixels[1] = wheel((mode_phase + 128) & 255)          
            neopixels.show()
