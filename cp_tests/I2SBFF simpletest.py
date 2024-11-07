# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
"""
import time
import board
import audiobusio

import synthio

print("I2SBFF simpletest.py")

MIDI_NOTE = 45

print("init I2S Output")
audio = audiobusio.I2SOut(bit_clock=board.A2, word_select=board.A1, data=board.A0)

print("setup synthio")
synth = synthio.Synthesizer(sample_rate=44100)
audio.play(synth)


for x in range(10):
    print("note on")
    synth.press(MIDI_NOTE)
    time.sleep(0.5)

    print("note off")
    synth.release(MIDI_NOTE)
    time.sleep(0.5)


print("release_displays")
import displayio

displayio.release_displays()


while True:
    print("note on")
    synth.press(MIDI_NOTE)
    time.sleep(0.5)

    print("note off")
    synth.release(MIDI_NOTE)
    time.sleep(0.5)
