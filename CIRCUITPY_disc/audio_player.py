import time

import re

import digitalio
import board
import busio
from adafruit_rfm import rfm69
import wifi

import helper

MAC = wifi.radio.mac_address.hex(":")

class Artefact:
    # REGEX_PACKET = re.compile(r'MAC\:(?P<mac_address>.*);TX:(?P<tx_power>.*)')
    # named groups are not supported in CircuitPython...
    REGEX_PACKET = re.compile(r'MAC\:(.*);TX:(.*)')

    def __init__(self, *, packet_text=None, mac_address=None, tx_power=None, last_rssi=None):
        self.packet_text = packet_text
        self.mac_address = mac_address
        self.tx_power = tx_power
        self.last_rssi = last_rssi

        if packet_text:
            self.parse_packet_text(packet_text)

    @property
    def mac_address_short(self):
        return self.mac_address[-5:]

    def parse_packet_text(self, packet_text):
        try:
            # groups = REGEX_PACKET.match(packet).groupdict()
            groups = self.REGEX_PACKET.match(packet_text).groups()
            self.mac_address = groups[0]
            self.tx_power = groups[1]
        except AttributeError as e:
            print(e)


class MagicQuestCrystal:
    """MagicQuestCrystal."""

    def __init__(self):
        super(MagicQuestCrystal, self).__init__()
        print(8 * "\n")
        print(42 * "*")
        print("MagicQuestCrystal")
        print("  https://github.com/s-light/magic_quest")
        print(42 * "*")

        print("device id (MAC)", MAC)

        self.receive_timeout = 0.1
        self.ping_interval = 1
        self.ping_next = time.monotonic()

        print("rfm69 init")
        CS = digitalio.DigitalInOut(board.A2)
        RESET = digitalio.DigitalInOut(board.A3)
        # IRQ = digitalio.DigitalInOut(board.A5)
        # IRQ.direction = digitalio.Direction.INPUT

        self.rfm1 = rfm69.RFM69(
            spi=board.SPI(),
            cs=CS,
            rst=RESET,
            frequency=433.0,
        )
        self.rfm1.radiohead = False
        # this disables the automatic radiohead header
        # this should make it easier to be compatible with the lowpowerlab arduino lib.
        print("rfm1 done.")

        print(f"Temperature: {self.rfm1.temperature}°C")
        print(f"Frequency: {self.rfm1.frequency_mhz}MHz")
        print(f"Bit rate: {self.rfm1.bitrate / 1000}kbit/s")
        print(f"Frequency deviation: {self.rfm1.frequency_deviation / 1000:0.1f}kHz")
        print(f"TX Power: {self.rfm1.tx_power:0.1f}dBm")

        CS2 = digitalio.DigitalInOut(board.A0)
        RESET2 = digitalio.DigitalInOut(board.A1)
        self.rfm2 = rfm69.RFM69(
            spi=board.SPI(),
            cs=CS2,
            rst=RESET2,
            frequency=433.0,
        )
        self.rfm2.radiohead = False
        print("rfm2 done.")

        print(f"Temperature: {self.rfm2.temperature}°C")
        print(f"Frequency: {self.rfm2.frequency_mhz}MHz")
        print(f"Bit rate: {self.rfm2.bitrate / 1000}kbit/s")
        print(f"Frequency deviation: {self.rfm2.frequency_deviation / 1000:0.1f}kHz")
        print(f"TX Power: {self.rfm2.tx_power:0.1f}dBm")

    ##########################################
    # communication

    # def send_ping(self, *, tx_power=13.0):
    #     # property tx_power: int
    #     # The transmit power in dBm.
    #     # Can be set to a value from
    #     #     -2 to 20 for high power devices (RFM69HCW, high_power=True) or
    #     #     -18 to 13 for low power devices.
    #     # Only integer power levels are actually set (i.e. 12.5 will result in a value of 12 dBm).
    #     self.rfm.tx_power = tx_power
    #     msg = f"MAC:{MAC};TX:{self.rfm.tx_power:+03.0f}"
    #     print(f"send '{msg}'")
    #     self.rfm.send(bytes(msg, "utf-8"))

    # def handle_ping(self):
    #     if time.monotonic() > self.ping_next:
    #         self.ping_next = time.monotonic() + self.ping_interval
    #         # The transmit power in dBm.
    #         # Can be set to a value from -2 to 20
    #         self.send_ping(tx_power=20.0)
    #         time.sleep(0.2)
    #         # self.send_ping(tx_power=13.0)
    #         # time.sleep(0.1)
    #         # self.send_ping(tx_power=0.0)
    #         # time.sleep(0.1)
    #         self.send_ping(tx_power=-2.0)
    #         # time.sleep(0.1)

    def handle_receive(self):
        # Wait for a packet to be received (up to 0.5 seconds)
        packet = self.rfm1.receive(timeout=self.receive_timeout)
        if packet is not None:
            packet_text = str(packet, "utf-8")
            device = Artefact(packet_text=packet_text, last_rssi=self.rfm1.last_rssi)
            print(
                # f"r: {packet_text[-12:]} " +
                f"r1: {device.mac_address_short} {device.tx_power} "
                + f"(rssi:{device.last_rssi:0.1f}dBm = "
                + f"{helper.map_to_01_constrained(device.last_rssi, -100.0, -27.0):0.1f})"
            )
        packet = self.rfm2.receive(timeout=self.receive_timeout)
        if packet is not None:
            packet_text = str(packet, "utf-8")
            device = Artefact(packet_text=packet_text, last_rssi=self.rfm2.last_rssi)
            print(
                # f"r: {packet_text[-12:]} " +
                f"r2: {device.mac_address_short} {device.tx_power} "
                + f"(rssi:{device.last_rssi:0.1f}dBm = "
                + f"{helper.map_to_01_constrained(device.last_rssi, -100.0, -27.0):0.1f})"
            )

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
        self.handle_receive()
        # self.handle_ping()

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
