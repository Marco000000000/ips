from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.oled.device import sh1106

# display
# serial = i2c(port=1, address=0x3C)#uncomment for i2c display
serial = spi(device=0, port=0)

device = sh1106(serial)
virtual = viewport(device, width=device.width, height=768)


def scrivi(a, b, c, d, e):
    with canvas(virtual) as draw:
        draw.text((3, 0), a, fill="white")
        draw.text((3, 10), b, fill="white")
        draw.text((3, 20), c, fill="white")
        draw.text((3, 30), d, fill="white")
        draw.text((3, 40), e, fill="white")
