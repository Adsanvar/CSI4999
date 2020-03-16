from gpiozero import LED
from time import sleep


gpio = LED(17)

def GPIOon():
    gpio.on()
    sleep(10)
    GPIOoff()


def GPIOoff():
    gpio.off()
