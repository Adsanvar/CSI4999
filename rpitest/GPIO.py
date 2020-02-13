from gpiozero import LED
from time import sleep

lock_pin = lock_pin(17)
#
def GPIOon():
    lock_pin.on()
    sleep(10)
    GPIOoff()
    

def GPIOoff():
    lock_pin.off()


    