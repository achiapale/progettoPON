from microbit import *
import radio

#configurazione del gruppo di comunicazione radio
radio.config(group = 2)
radio.on()

#ciclo infinito
while True:
    message = radio.receive()
    if message:
        display.show(message)
        print(message)
    if button_a.is_pressed():
        radio.off()
