from time import sleep_ms
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(-1, Pin(4),Pin(5),freq=400000) # Bitbanged I2C bus
assert 60 in i2c.scan(), "No OLED display detected!"
oled = SSD1306_I2C(128, 64, i2c)
buf = "wubba lubba dub dub  "
oled.invert(0) # White text on black background
oled.contrast(255) # Maximum contrast
j = 0

while True:
    oled.fill(0)
    oled.text(buf[j%len(buf):]+buf, 10, 10)
    oled.show()
    sleep_ms(20)
    j += 1
