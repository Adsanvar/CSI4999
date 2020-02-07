from gpiozero import LED
from time import sleep

def GPIOon():
    gpio = LED(17)
    switchon = gpio.on()
    

def GPIOoff():
    gpio = LED(17)
    switchoff = gpio.off()