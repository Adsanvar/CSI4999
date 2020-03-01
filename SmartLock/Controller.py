#from gpiozero import LED
from time import sleep


led = LED(17)


def on():
    led.on()
    sleep(10)
    off()

def off():
    led.off()
