# cp_audio_player
experiments with wm8960

forum posts:
- [is the Adafruit Voice Bonnet *compatible* with ESP32 S3 CP devices?](https://forums.adafruit.com/viewtopic.php?p=1007149)
- [CP ESP32-S3 with WM8960 - how to trouble-shoot](https://forums.adafruit.com/viewtopic.php?p=)


## hw

- [Adafruit Voice Bonnet](https://learn.adafruit.com/adafruit-voice-bonnet/overview)
- [Adafruit ESP32-S3 Reverse TFT Feather](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/)

### connection

| bonnet    | function     | cable  | feather |
| --------- | ------------ | ------ | ------- |
| QUICK     | GND/3.3V/I2C |        | QUICK   |
| 5V        | amp power    | orange | USB     |
| I2S_BCRK  | bit_clock    | green  | A0      |
| I2S_LRCRK | word_select  | blue   | A1      |
| I2S_DOUT  | data out     | orange | A2      |
| I2S_DIN   | data in      | -      | A3      |

