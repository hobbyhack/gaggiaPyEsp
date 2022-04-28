import time

import network
import webrepl
from machine import Pin, SoftI2C, SoftSPI

import max31865
import sh1106
import utils
from hx711 import HX711
from secret import WIFI_PASSWORD, WIFI_SSID


def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    # print("network config:", sta_if.ifconfig())
    return sta_if


def load_i2c():
    print("loading 12c bus")
    return SoftI2C(scl=Pin(22), sda=Pin(21))


def load_oled(bus):
    print("loading oled")
    OLED_WIDTH = 128
    OLED_HEIGHT = 64
    return sh1106.SH1106_I2C(OLED_WIDTH, OLED_HEIGHT, bus)


def load_hx711():
    return HX711(d_out=5, pd_sck=4)


def load_spi():
    spi = SoftSPI(
        -1,
        sck=Pin(18, Pin.OUT),
        mosi=Pin(23, Pin.OUT),
        miso=Pin(19, Pin.OUT),
    )
    spi.init(baudrate=115200, polarity=0, phase=1)
    return spi


def load_max31865(bus):
    cs = Pin(17)
    temp = max31865.MAX31865(bus, cs)
    return temp


sta_if = wifi_connect()
webrepl.start()

i2c = load_i2c()
spi = load_spi()
oled = load_oled(bus=i2c)
scale = load_hx711()
temp = load_max31865(bus=spi)

# time.sleep(1)
utils.scale_temp(scale, temp, oled)
