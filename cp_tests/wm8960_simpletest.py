# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Cooper Dalrymple
#
# SPDX-License-Identifier: Unlicense

# based on https://github.com/adafruit/Adafruit_CircuitPython_WM8960/blob/main/examples/wm8960_simpletest.py

"""
Demonstrates I2C Output on WM8960 Codec by generating a simple tone using synthio. Sounds like an
alarm clock.
"""

import time
import board
import digitalio
import audiobusio
import synthio
from adafruit_wm8960 import WM8960


print("wm8960_simpletest.py")

print("init WM8960 I2C")
codec = WM8960(board.I2C(), 44100, 16)
codec.volume = 1.0
codec.headphone = 0.5
codec.speaker = 0.1

print("init I2S Output")
audio = audiobusio.I2SOut(bit_clock=board.A0, word_select=board.A1, data=board.A2)
# board.A3 = data_in

print("setup synthio")
synth = synthio.Synthesizer(sample_rate=codec.sample_rate)
audio.play(synth)

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

while True:
    print("note on")
    synth.press(29)  # midi note 65 = F0
    led.value = True
    time.sleep(0.5)
    synth.release(65)  # release the note we pressed
    led.value = False
    print("note off")
    time.sleep(0.5)
