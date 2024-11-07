# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
"""
import board
import audiobusio
import audiomp3
import audiocore

audio = audiobusio.I2SOut(board.A2, board.A1, board.A0)

print(".")

# filename = "music/test_loop.wav"
filename = "music/185487__mika55__wiodubstep-loop005.mp3"

if (filename.endswith('.wav')):
    print("wav file")
    audio_data = audiocore.WaveFile(open(filename, "rb"))
elif (filename.endswith('.mp3')):
    print("mp3")
    audio_data = audiomp3.MP3Decoder(open(filename, "rb"))
else:
    print("unknown")
    audio_data = False


# Update to True loop playback. False plays once.
LOOP = True
print("Playing audio_data")
audio.play(audio_data, loop=LOOP)
while audio.playing:
    pass

print("Done playing!")
