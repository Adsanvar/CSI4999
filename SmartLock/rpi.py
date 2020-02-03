from gpiozero import LED
from time import sleep

def open(gpio):
    gpio.on()
    sleep(10)

def close(gpio):
    gpio.off()
        

