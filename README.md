# Hello MicroPython

## Getting started

MicroPython project skeleton

```
git clone http://git.k-space.ee/lauri/micropython-skeleton
cd micropython-skeleton
make
```

First let's some LED-s blinking.
Press Ctrl-E for paste mode, otherwise spaces get mangled.
Press Ctrl-Shift-V for pasting.
Press Ctrl-D to exit paste mode and evaluate the code.

```
from time import sleep
from machine import Pin

# RGB LED is connected to programmable pins 12, 13, 15
led_red = Pin(12, Pin.OUT)
led_green = Pin(13, Pin.OUT)
led_blue = Pin(15, Pin.OUT)

# The values are inverted because 3.3v is common pin
led_red.value(1)
led_green.value(1)
led_blue.value(1)

for j in range(0, 5):
    led_red.value(0)
    sleep(1)
    led_red.value(1)
    led_green.value(0)
    sleep(1)
    led_green.value(1)
    led_blue.value(0)
    sleep(1)
    led_blue.value(1)
```

Tasks:

1. Modify the code so yellow, cyan, magenda and white would be included.



# Button presses

On the board there is button labelled "Boot", this is hooked up to pin 2.
By default there is a resistor which pulls the voltage on the pin to 3.3v, but when button is pressed the pin is shorted to ground so the voltage goes to 0v.
Most modern solutions use interrupts to detect voltage change on the pin:

```
from machine import Pin
from time import sleep

Pin(12, Pin.OUT).value(1)
Pin(13, Pin.OUT).value(1)
led_blue = Pin(15, Pin.OUT)
button = Pin(0)

turned_off = False

def callback(p):
    global turned_off
    turned_off = not turned_off
    led_blue.value(turned_off)

# Execute function 'callback' when voltage goes from 3.3v to 0v on pin 0
button.irq(trigger=Pin.IRQ_FALLING, handler=callback)
```

Tasks:

1. Modify the code so pressing button shuffles between off, red, green, blue, yellow, cyan, magenta and white



# Driving OLED screens

Let's get some pixels on the screen.
There's 128x64 pixels monochrome OLED screen connected via I2C bus on the pins 4 and 5.

```
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(-1, Pin(4),Pin(5), freq=400000) # Bitbanged I2C bus
oled = SSD1306_I2C(128, 64, i2c)
oled.invert(0) # White text on black background
oled.contrast(255) # Maximum contrast

oled.fill(0)
name = "Lauri"
oled.text("Hi %s" % name, 10, 10)
oled.show()
```

Tasks:

1. When button is pressed show a corresponding message on the screen - lights turned on/off or the name of the color shown

## Temperature & humidity

Next let's hook up DHT11 sensor to the board and measure the temperature.

```
from time import sleep
from machine import Pin
from dht import DHT11

d = DHT11(Pin(4))

try:
  d.measure()
except OSError:
  print("Sensor not connected")
else:
  print("Temperature %sC" % d.temperature())
  print("Humidity %s%%" % d.humidity())
finally:
  sleep(1)
```

Tasks:

1. Get temperature and humidity displayed on the screen

## Connecting to internet

Exit the serial console by pressing Ctrl-A and then Ctrl-Q.
Upload module to handle WebSockets and return to Python prompt:

```
ampy -p /dev/ttyUSB0 put uwebsockets.py
ampy -p /dev/ttyUSB0 put boot.py # Script that connects to itcollege network
make console
```

Press EN button on the board to reset the board.

Paste following:

```
import sys
import uwebsockets
from machine import Pin

Pin(12, Pin.OUT).value(1)
Pin(13, Pin.OUT).value(1)
led_blue = Pin(15, Pin.OUT)

channel = "living-room-of-lauri"
uri = "ws://iot.koodur.com:80/ws/" + channel
print("Connecting to:", uri)
conn = uwebsockets.connect(uri)
conn.send("alive")

turned_off = False

while True:
    print("Reading message...")
    fin, opcode, data = conn.read_frame()
    if data == "toggle":
        turned_off = not turned_off
        led_blue.value(turned_off)
    else:
        print("Got unknown command:", data)
```

Using web browser navigate [here](http://iot.koodur.com/demo2.html#living-room-of-lauri)

1. Move to another channel to prevent flipping lights in my living room
2. Improve the code so the "Boot" button and button in the web interface both work simultaneously
3. Download the HTML file and add buttons to select different colors, adjust Python code to handle new commands


# Summary

ESP32 microcontroller with MicroPython is a really cheap way to get started with the IoT stuff. See more detailed information [here](https://lauri.xn--vsandi-pxa.com/2017/06/espressif.html).

Some more tricks to try:

* Add dimming of LED-s with PWM
* Add [colorpicker](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/color)

Other interesting projects with ESP8266 and ESP32 microcontrollers:

* [Nixie clock](https://github.com/k-space-ee/nixiesp12) with ESP8266
* [Sumorobot](http://robot.itcollege.ee/sumorobot/2017/08/25/sumesp-prototype/) with ESP32 