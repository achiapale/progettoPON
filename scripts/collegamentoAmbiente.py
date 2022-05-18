from microbit import *
import radio

#configurazione del gruppo di comunicazione radio 
radio.config(group = 1)
radio.on()

#ciclo infinito
while True:
    message = radio.receive()
    if message:
        print(message)
        display.show(message)
        sleep(100)
