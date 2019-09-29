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

Author(s): Don Korte

this version uses TFT display, and requires an M4 class ItsyBitsy
must create lib/ folder and install the following Adafruit libraries:
    adafruit_display_text (folder)
    adafruit_display_shapes (folder)
    adafruit_st7735r.mpy
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

_version__ = "2.0.0"
__repo__ = "https://github.com/dnkorte/blinky_eyes"

import board
import time
from digitalio import DigitalInOut, Direction, Pull
import displayio
import terminalio
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
import neopixel

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
# neopixels[0] = RED
# neopixels[1] = RED
# neopixels.show()



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

# Draw smaller inner rectangles to represent left LED
left_bitmap = displayio.Bitmap(30, 15, 1)
left_palette = displayio.Palette(1)
left_palette[0] = D_RED
left_sprite = displayio.TileGrid(left_bitmap,
                                  pixel_shader=left_palette,
                                  x=35, y=25)
splash.append(left_sprite)

leftb_bitmap = displayio.Bitmap(30, 15, 1)
leftb_palette = displayio.Palette(1)
leftb_palette[0] = D_RED
leftb_sprite = displayio.TileGrid(leftb_bitmap,
                                  pixel_shader=leftb_palette,
                                  x=35, y=40)
splash.append(leftb_sprite)

#  Draw smaller inner rectangles to represent right LED
right_bitmap = displayio.Bitmap(30, 15, 1)
right_palette = displayio.Palette(1)
right_palette[0] = D_RED
right_sprite = displayio.TileGrid(right_bitmap,
                                  pixel_shader=right_palette,
                                  x=95, y=25)
splash.append(right_sprite)

rightb_bitmap = displayio.Bitmap(30, 15, 1)
rightb_palette = displayio.Palette(1)
rightb_palette[0] = D_RED
rightb_sprite = displayio.TileGrid(rightb_bitmap,
                                  pixel_shader=rightb_palette,
                                  x=95, y=40)
splash.append(rightb_sprite)


text_group = displayio.Group(max_size=10, scale=2, x=11, y=94)
# text_group = displayio.Group(max_size=10, scale=2, x=11, y=48)
text = ""
modenum_textbox = label.Label(terminalio.FONT, text=text, color=0xFFFF00, max_glyphs=12)
text_group.append(modenum_textbox) # Subgroup for text scaling

splash.append(text_group)

# setup environment #################################################################
mode = 0
mode_initiated = False
mode_duration_counter = 0
mode_phase = 0
HIGHEST_MODE = 9
icon_counter = 0

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Digital input with pullup on D7
button = DigitalInOut(board.D11)
button.direction = Direction.INPUT
button.pull = Pull.UP

left_icon = [ D_RED, D_RED, D_RED, D_RED ]
right_icon = [ D_RED, D_RED, D_RED, D_RED ]

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

    icon_counter += 1
    if icon_counter > 3:
        icon_counter = 0
    left_palette[0] = left_icon[icon_counter]
    right_palette[0] = right_icon[icon_counter]

    if mode == 0:                   # both solid red
        if not mode_initiated:
            neopixels[0] = RED
            neopixels[1] = RED
            neopixels.show()
            mode_initiated = True
            modenum_textbox.text = " 0 RR Solid"
            left_icon = [ D_RED, D_RED, D_RED, D_RED ]
            right_icon = [ D_RED, D_RED, D_RED, D_RED ]
            # left_palette[0] = D_RED
            # leftb_palette[0] = D_RED
            # right_palette[0] = D_RED
            # rightb_palette[0] = D_RED

    elif mode == 1:                 # both solid green
        if not mode_initiated:
            neopixels[0] = GREEN
            neopixels[1] = GREEN
            neopixels.show()
            mode_initiated = True
            modenum_textbox.text = " 1 GG Solid"
            left_icon = [ D_GREEN, D_GREEN, D_GREEN, D_GREEN ]
            right_icon = [ D_GREEN, D_GREEN, D_GREEN, D_GREEN ]
            # left_palette[0] = D_GREEN
            # leftb_palette[0] = D_GREEN
            # right_palette[0] = D_GREEN
            # rightb_palette[0] = D_GREEN

    elif mode == 2:                 # both solid blue
        if not mode_initiated:
            neopixels[0] = BLUE
            neopixels[1] = BLUE
            neopixels.show()
            mode_initiated = True
            modenum_textbox.text = " 2 BB Solid"
            modenum_textbox.text = " 1 GG Solid"
            left_icon = [ D_BLUE, D_BLUE, D_BLUE, D_BLUE ]
            right_icon = [ D_BLUE, D_BLUE, D_BLUE, D_BLUE ]
            # left_palette[0] = D_BLUE
            # leftb_palette[0] = D_BLUE
            # right_palette[0] = D_BLUE
            # rightb_palette[0] = D_BLUE

    elif mode == 3:                 # both solid yellow
        if not mode_initiated:
            neopixels[0] = YELLOW
            neopixels[1] = YELLOW
            neopixels.show()
            mode_initiated = True
            modenum_textbox.text = " 3 YY Solid"
            left_icon = [ D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW ]
            right_icon = [ D_YELLOW, D_YELLOW, D_YELLOW, D_YELLOW ]
            # left_palette[0] = D_YELLOW
            # leftb_palette[0] = D_YELLOW
            # right_palette[0] = D_YELLOW
            # rightb_palette[0] = D_YELLOW

    elif mode == 4:                 # flipping red / green
        if not mode_initiated:
            neopixels[0] = RED
            neopixels[1] = GREEN
            mode_phase = 1          # for this mode phase 0 is R/G, phase 1 is G/R
            neopixels.show()
            mode_initiated = True
            modenum_textbox.text = " 4 RG Flip"
            left_icon = [ D_RED, D_RED, D_GREEN, D_GREEN ]
            right_icon = [ D_GREEN, D_GREEN, D_RED, D_RED ]
            # left_palette[0] = D_RED
            # leftb_palette[0] = D_GREEN
            # right_palette[0] = D_GREEN
            # rightb_palette[0] = D_RED
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
            modenum_textbox.text = " 5 YY Flash"
            left_icon = [ D_YELLOW, D_YELLOW, D_BLACK, D_BLACK ]
            right_icon = [ D_YELLOW, D_YELLOW, D_BLACK, D_BLACK ]
            # left_palette[0] = D_YELLOW
            # leftb_palette[0] = D_BLACK
            # right_palette[0] = D_BLACK
            # rightb_palette[0] = D_YELLOW
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
            modenum_textbox.text = " 6 BY Flip"
            left_icon = [ D_BLUE, D_BLUE, D_YELLOW, D_YELLOW ]
            right_icon = [ D_YELLOW, D_YELLOW, D_BLUE, D_BLUE ]
            # left_palette[0] = D_BLUE
            # leftb_palette[0] = D_YELLOW
            # right_palette[0] = D_YELLOW
            # rightb_palette[0] = D_BLUE
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

    elif mode == 7:                 # pulsing orange and white for pumpkin eyes
        if not mode_initiated:
            neopixels[0] = ORANGE
            neopixels[1] = ORANGE
            neopixels.show()
            mode_initiated = True
            modenum_textbox.text = " 7 Pumpkin"
            left_icon = [ D_ORANGE, D_ORANGE, D_ORANGE, D_WHITE ]
            right_icon = [ D_ORANGE, D_ORANGE, D_ORANGE, D_WHITE ]
            # left_palette[0] = D_ORANGE
            # leftb_palette[0] = D_WHITE
            # right_palette[0] = D_ORANGE
            # rightb_palette[0] = D_WHITE
        else:
            # if mode_duration_counter < 2:
            #     neopixels[0] = ORANGE
            #     neopixels[1] = ORANGE
            #     neopixels.show()
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
            # neopixels.show()
            if mode_duration_counter > 49:
                neopixels[0] = ORANGE
                neopixels[1] = ORANGE
                neopixels.show()
                mode_duration_counter = 0


    elif mode == 8:                 # fast flipping red / green
        if not mode_initiated:
            neopixels[0] = RED
            neopixels[1] = GREEN
            mode_phase = 1          # for this mode phase 0 is R/G, phase 1 is G/R
            neopixels.show()
            mode_initiated = True
            modenum_textbox.text = " 8 RG FastF"
            left_icon = [ D_RED, D_GREEN, D_RED, D_GREEN ]
            right_icon = [ D_GREEN, D_RED, D_GREEN, D_RED ]
            # left_palette[0] = D_RED
            # leftb_palette[0] = D_GREEN
            # right_palette[0] = D_GREEN
            # rightb_palette[0] = D_RED
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

    elif mode == 9:                 # test colors mode
        if not mode_initiated:
            r = 0
            g = 0
            neopixels[0] = (r, g, 0)
            neopixels[1] = (r, g, 100)
            neopixels.show()
            mode_initiated = True
            modenum_textbox.text = " 9 COLORTST"
            left_icon = [ D_RED, D_GREEN, D_YELLOW, D_BLUE ]
            right_icon = [ D_BLUE, D_YELLOW, D_GREEN, D_RED ]
            # left_palette[0] = D_RED
            # leftb_palette[0] = D_GREEN
            # right_palette[0] = D_GREEN
            # rightb_palette[0] = D_RED
        else:
            r += 5
            if r > 255:
                g += 5
                r = 0
            neopixels[0] = (r, g, 0)
            neopixels[1] = (r, g, 100)            
            neopixels.show()
            print("r="+str(r)+" g="+str(g))

    time.sleep(0.1)
