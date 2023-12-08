from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106
from luma.core.virtual import viewport
import RPi.GPIO as GPIO

#display

#serial = spi(device=0,port=0) #uncomment for spi display
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
virtual = viewport(device, width=device.width, height=768)

def scrivi(a,b,c,d,e):
    with canvas(virtual) as draw:
        draw.text((3, 0), a, fill="white")
        draw.text((3, 10), b, fill="white")
        draw.text((3, 20), c, fill="white")
        draw.text((3, 30), d, fill="white")
        draw.text((3, 40), e, fill="white")
