from gpiozero import LED
from time import sleep

def GPIOon():
    gpio = LED(17)
    gpio.on()
    sleep(10)
    GPIOoff()


def GPIOoff():
    gpio = LED(17)
    gpio.off()
