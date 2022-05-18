#misurazione della temperatura di un termosifone

from microbit import *
import radio
#import time
#import os

TEMP_MINIMA_PRESENZA = 24
TEMP_MASSIMA_PRESENZA = 29
TEMP_ASSENZA = 20
TEMP_NOTTE = 15


# funzione per verificare se è giorno
def verifyDay():
    # try
    if display.read_light_level() < 100:
        d = False
    else:
        d = True
    return d


# funzione per misurare la temperatura
def measureTemperature():
    t = temperature()
    return t


# funzione che indica la presenza di persone
def findPeople():
    # se il microfono sente dei rumori
    if microphone.was_event(SoundEvent.LOUD):
        p = True
    else:
        p = False
    return p


while True:
    day = verifyDay()

    temp = measureTemperature()

    # stampa la temperatura
    # print("Temperatura: ")
    # print(temp)

    people = findPeople()

    radio.config(group = 1)
    radio.on()
    stringa = str(day)+';'+str(temp)+';'+str(people)+';'
    print(stringa)
    radio.send(stringa)
    sleep(1000)

    # stampa la presenza o meno di persone
    if people:
        print("Ci sono persone nella stanza. ")
    else:
        print("Non ci sono persone nella stanza. ")
    if day:
        # verifica la presenza di persone
        if people:
            # verifica che la tempertur sia nel range corretto
            if temp < TEMP_MINIMA_PRESENZA:
                print("temperatura troppo bassa: ")
                print(temp)
            elif temp > TEMP_MASSIMA_PRESENZA:
                print("temperatura troppo alta: ")
                print(temp)
            else:
                print("temperatura adeguata")
        # verifica se la temperatura è elevata in assenza di persone
        elif temp > TEMP_ASSENZA:
            print("abbassare, temperatura troppo elevata: ")
            print(temp)
        else:
            print("temperatura adeguata")
    # vericia se la temperatura notturna è adeguata
    elif temp > TEMP_NOTTE:
        print("abbassare, e' notte: ")
        print(temp)
    else:
        print("temperatura adeguata")
    sleep(1000)
