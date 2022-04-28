# gaggiaPyEsp

Gaggia Classic Pro MicroPython controller

# Pins

https://randomnerdtutorials.com/esp32-pinout-reference-gpios/

## Digital Inputs

returns 0 or 1
0=false=LOW
0=true=HIGH

- 0-.8V = 0
- 0.8-2.4V = ?
- 2.4-3.3V = 1

- pulled high during bootup

### Best Pins

    GPIO4, GPIO13, GPIO16-GPIO33

### floating pins

Pullup Pins:
GPIO0 - GPIO5
GPIO12 - GPIO33
works but careful:
GPIO0-GPIO3, GPIO5, GPIO12, GPIO14, GPIO15

Pulldown Pins:
GPIO4 - GPIO5
GPI12 - GPI39
works but careful:
GPIO5, GPI12, GPI14, GPI15

Notes
GPIO0 - outputs PWM at boot
GPIO1 - TX pin debug output at boot
GPIO2 - Onboard LED
GPIO3 - High at boot
GPIO5 - output pwn at boot
GPIO12 - Boot fail if pulled high
GPIO14 - outputs PWM at boot
GPIO15 - outputs PWM at boot

need a pullup (default high) or pulldown resistor (default low)

## Digital Outputs

3.3V (HIGH) out or OV out (LOW/ground)

## Output Pins

### Best Pins

    GPIO4, GPIO13, GPIO16-GPIO33

### Works but be careful

    GPIO2, GPIO4, GPIO12, GPIO16-GPIO33

## Analog Inputs

between 0 - 3.3V
12 bit resulution: 0-4096 (.8mV)
GPIO32-GPIO36, GPIO39

## Analog Outputs

PWM 3.3V

DACs - 0-3.3V
DAC1 (GPIO25)
DAC2 (GPIO26)

# OLED

https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/
this is my bord
https://github.com/robert-hh/SH1106 - not the one in the article

from machine import Pin, SoftI2C
import sh1106
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c)

oled.text('Hello, World 1!', 0, 0)
oled.text('Hello, World 2!', 0, 10)
oled.text('Hello, World 3!', 0, 20)
oled.show()

oled.fill(1)
oled.show()

oled.fill(0)
oled.show()

while True:
weight = round(((driver.read_average(10)+14412.94)/427.77925))
oled.fill(0)
oled.show()
oled.text(str(weight), 0, 0)
oled.show()

# Hx711

https://github.com/SergeyPiskunov/micropython-hx711

from hx711 import HX711
driver = HX711(d_out=5, pd_sck=4)
print((driver.read()+15248)/430.824)

driver.power_off()

from micropython import const
driver = HX711(d_out=5, pd_sck=4, channel=const(3))
print((driver.read()-183200)/238)

# MAX31865

https://medium.com/@epabrego/1-micropython-esp32-max31865-rtd-pt100-9e9c02e2b55d
https://git.arofarn.info/gitea/arofarn/Adafruit_MicroPython_MAX31685/src/branch/master/adafruit_max31865.py
https://git.arofarn.info/gitea/arofarn/Adafruit_MicroPython_MAX31685/src/branch/master/examples/max31865_simpletest.py
https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/arduino-code

import time
import machine
import max31865

# Initialize SPI bus and sensor.
SPI = machine.SoftSPI(-1, sck=machine.Pin(18, machine.Pin.OUT),
mosi=machine.Pin(23, machine.Pin.OUT),
miso=machine.Pin(19, machine.Pin.OUT)
)
SPI.init(baudrate=115200, polarity=0, phase=1)
CS = machine.Pin(17)
SENSOR = max31865.MAX31865(SPI, CS)
# Note you can optionally provide the thermocouple RTD nominal, the reference
# resistance, and the number of wires for the sensor (2 the default, 3, or 4)
# with keyword args:
# sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=2)

# Main loop to print the temperature every second.
while True:
# Read temperature.
TEMP = SENSOR.temperature
# Print the value.
print("Temperature: {0:0.3f}C".format(TEMP))
# Delay for a second.
time.sleep(1.0)
