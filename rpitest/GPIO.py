from gpiozero import LED
from time import sleep

def GPIOon(x):
    x = LED(17)
    x = x.on()
    

def GPIOoff(y):
    y = LED(17)
    y = y.off()


    