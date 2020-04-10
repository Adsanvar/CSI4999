from gpiozero import LED
from time import sleep

#pin
gpio = LED(17)

def GPIOon(timer):
    gpio.on()
    sleep(timer)
    GPIOoff()

def GPIOoff():
    gpio.off()
