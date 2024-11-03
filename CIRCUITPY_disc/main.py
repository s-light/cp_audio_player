#!/usr/bin/env python3
# coding=utf-8

"""
AudioPlayer

HW:
- ESP32-S3 based (Adafruit Reverse TFT )
- WM8960 (Adafruit Voice Bonnet)
"""

# add src as import path
import sys

sys.path.append("/src")

import time
import board
import displayio

from audio_player import AudioPlayer


def wait_with_print(wait_duration=5, step_duration=0.25):
    for index in range(wait_duration * step_duration):
        print(".", end="")
        time.sleep(step_duration / wait_duration)


def main():
    """Main handling."""
    print(4 * "\n")
    wait_with_print(10)
    print("")
    print(42 * "*")
    print("Python Version: " + sys.version)
    print("board: " + board.board_id)
    print(42 * "*")

    # deactivate display.
    # if hasattr(board, "DISPLAY"):
    #     # print("deactivate display backlight.")
    #     # board.DISPLAY.brightness = 0
    #     print("deactivate display.")
    #     displayio.release_displays()

    myAudioPlayer = AudioPlayer()
    myAudioPlayer.run()

    # start = time.monotonic()
    # heartbeat_last = time.monotonic()
    # while (time.monotonic() - start) < 10:
    #     time.sleep(0.1)
    #     if (time.monotonic() - heartbeat_last) > 1:
    #         heartbeat_last = time.monotonic()
    #         print(heartbeat_last)
    print("done.")
    wait_with_print(10)
    print("\nexit.")


##########################################
if __name__ == "__main__":
    main()
