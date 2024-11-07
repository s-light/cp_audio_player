# SPDX-FileCopyrightText: Copyright (c) 2024 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

# based on https://github.com/adafruit/Adafruit_CircuitPython_WM8960/blob/main/examples/wm8960_simpletest.py

"""
WM8960 Codec playing mp3 and wav
"""


import time

import re

import board
import digitalio

import audiobusio
import synthio
import audiomp3
import audiocore

from adafruit_wm8960 import WM8960

import helper


class AudioPlayer:
    """AudioPlayer."""

    MIDI_NOTE = 45

    def __init__(self):
        super(AudioPlayer, self).__init__()
        print(8 * "\n")
        print(42 * "*")
        print("AudioPlayer")
        print("  https://github.com/s-light/cp_audio_player")
        print(42 * "*")

        self.led = digitalio.DigitalInOut(board.LED)
        self.led.switch_to_output()

        print("audio init")
        self.codec = WM8960(board.STEMMA_I2C(), 44100, 16)
        self.codec.volume = 1.0
        self.codec.headphone = 0.2
        self.codec.speaker = 0.1

        print("init I2S Output")
        self.audio = audiobusio.I2SOut(bit_clock=board.A2, word_select=board.A1, data=board.A0)

        print("setup synthio")
        self.synth = synthio.Synthesizer(sample_rate=self.codec.sample_rate)
        
        self.audio.play(self.synth)

    ##########################################
    # ui / button handling

    def handle_button(self, event):
        # print("\n"*5)
        # print(event)
        # print("\n"*5)
        if event.pressed and event.key_number == 0:
            pass

    ##########################################
    # main handling

    def main_loop(self):
        # Small delay to keep things responsive but give time for interrupt processing.
        time.sleep(0)

        print("note on")
        self.synth.press(self.MIDI_NOTE)
        self.led.value = True
        time.sleep(0.5)

        self.synth.release(self.MIDI_NOTE)
        self.led.value = False
        # ne next sleep before the print helps to get a nicer release..
        # otherwise the update of the display seems to mess with the I2S signal generation...
        time.sleep(0.2)
        print("note off")
        time.sleep(0.3)

    def run(self):
        # self.userinput.update()
        print(42 * "*")
        print("run")
        # self.userinput.update()

        # if supervisor.runtime.serial_connected:
        # self.userinput.userinput_print_help()
        running = True
        while running:
            try:
                self.main_loop()
            except KeyboardInterrupt as e:
                print("KeyboardInterrupt - Stop Program.", e)
                running = False
