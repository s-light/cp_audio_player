# SPDX-FileCopyrightText: Copyright (c) 2022 Pete Lewis for SparkFun Electronics
# SPDX-FileCopyrightText: Copyright (c) 2024 Cooper Dalrymple
#
# SPDX-License-Identifier: MIT

# based on https://github.com/adafruit/Adafruit_CircuitPython_WM8960?tab=readme-ov-file#usage-example

# Monitor Stereo Input: INPUT1 => Output Mixer => Headphones


import time
import board
from adafruit_wm8960 import Input, WM8960

print("wm8960_simpletest_mic2headphone.py")

print("init WM8960 I2C")
codec = WM8960(board.I2C())

# Select the desired input.
# Available options are
# MIC1 (single-ended),
# MIC2 (differential),
# MIC3 (differential),
# LINE2,
# LINE3.
print("setup input as MIC1")
codec.input = Input.MIC1

# Configure the microphone boost gain
codec.gain = 0.9
# will be overwritten by alc

print("with direct routing to headphone")
# Bypass analog signal to analog output
codec.monitor = 1.0

# Enable the amplifier and set the output volume
codec.headphone = 0.9


while True:
    print("nothing to do...")
    time.sleep(10)
