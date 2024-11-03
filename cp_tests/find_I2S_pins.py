# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

# source: https://learn.adafruit.com/adafruit-metro-esp32-s3/i2s

"""
CircuitPython I2S Pin Combination Identification Script
"""
import board
import audiobusio
from microcontroller import Pin


SPECIAL_PINS = [
    # This is not an exhaustive list of unexposed pins. Your results
    # may include other pins that you cannot easily connect to.
    "NEOPIXEL",
    "DOTSTAR_CLOCK",
    "DOTSTAR_DATA",
    "APA102_SCK",
    "APA102_MOSI",
    "NEOPIXEL_POWER",
    "LED",
    "SWITCH",
    "BUTTON",
    # exclude pins with other functions
    # i2c
    "SDA",
    "SCL",
    "SDA1",
    "SCL1",
    # spi
    "MISO",
    "MOSI",
    "SCK",
    # serial
    "TX",
    "RX",
]

def is_hardware_i2s(bit_clock, word_select, data):
    try:
        p = audiobusio.I2SOut(bit_clock, word_select, data)
        p.deinit()
        return True
    except ValueError:
        return False


def get_unique_pins():
    exclude = [
        getattr(board, p)
        for p in SPECIAL_PINS
        if p in dir(board)
    ]
    pins = [
        pin
        for pin in [getattr(board, p) for p in dir(board)]
        if isinstance(pin, Pin) and pin not in exclude
    ]
    unique = []
    for p in pins:
        if p not in unique:
            unique.append(p)
    return unique


print("CircuitPython I2S Pin Combination Identification Script")
print("list pin combinations:")


for bit_clock_pin in get_unique_pins():
    for word_select_pin in get_unique_pins():
        for data_pin in get_unique_pins():
            if (
                bit_clock_pin is word_select_pin
                or bit_clock_pin is data_pin
                or word_select_pin is data_pin
            ):
                continue
            if is_hardware_i2s(bit_clock_pin, word_select_pin, data_pin):
                print(
                    "Bit clock pin:",
                    bit_clock_pin,
                    "\t Word select pin:",
                    word_select_pin,
                    "\t Data pin:",
                    data_pin,
                )
            else:
                pass
