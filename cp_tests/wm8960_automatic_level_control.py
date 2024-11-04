# SPDX-FileCopyrightText: Copyright (c) 2022 Pete Lewis for SparkFun Electronics
# SPDX-FileCopyrightText: Copyright (c) 2024 Cooper Dalrymple
#
# SPDX-License-Identifier: MIT

# based on https://github.com/adafruit/Adafruit_CircuitPython_WM8960/blob/main/examples/wm8960_automatic_level_control.py

import time
import board
from adafruit_wm8960 import Input, WM8960

codec = WM8960(board.I2C())
codec.input = Input.MIC1
codec.gain = 0.5
codec.volume = 1.0
codec.headphone = 0.8

codec.alc = True
codec.loopback = True

while True:
    time.sleep(1.0)
