from gpiozero import LED
from time import sleep

class Pin:

    def open(on):
        
        output = LED(17)
        output.on()
        sleep(15)
        ouput.off