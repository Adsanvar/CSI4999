from gpiozero import LED
from time import sleep

led = LED(17)

def GPIOon():
    led.on()
    sleep(10)
    GPIOoff()
    

def GPIOoff():
    led.off()


    