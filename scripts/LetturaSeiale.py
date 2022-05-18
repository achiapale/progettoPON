import threading, queue
import time
import os
import numpy as np
import sys
import serial, time
import csv

dataFile = "C:\\Users\\lucam\\Documents\\4BRob\\PON\\Dati.csv"
qAmb = queue.Queue() # CODA SERIALIZZATA PER LA RICEZIONE DEI DATI DELL'AMBIENTE
qTerm = queue.Queue() # CODA SERIALIZZATA PER LA RICEZIONE DEI DATI DEL TERMOSIFONE

def createCSV(dataFile): # FUNZIONE CHE CREA UN FILE CSV CON INTESTAZIONE
    with open(dataFile, 'w') as f:
        writer = csv.writer(f, delimiter = ',')
        header = (["Giorno/Notte", "Temperatura", "Persone", "Ambiente", "Data/Ora"])
        writer.writerow(header)
        f.close()

def addData(dataFile, data): # FUNZIONE CHE AGGIUNGE I DATI NEL FILE CSV
    with open(dataFile, 'a') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)
        f.close()

createCSV(dataFile) # RICHIAMO FUNZIONE PER LA CREAZIONE DEL CSV

class Read_Microbit_Termosifone(threading.Thread): # CLASSE THREAD PER MICROBIT TERMOSIFONE
    def _init_(self):
        threading.Thread._init_(self)
        self._running = True
      
    def terminate(self): # FUZIONE CHE TERMINA IL THREAD
        self._running = False
        
    def run(self): # FUNZIONE CHE PARTE ALLA CREAZIONE DEL THREAD
        #serial config
        port = "COM8"
        s = serial.Serial(port) # AVVIA IL COLLEGAMMENTO CON LA PORTA SERIALE PASSAT TRA PARAMETRI
        s.baudrate = 115200 # SETTAGGIO NUMERO DI BIT INVIATI
        self._running = True
        while self._running: # FINO A CHE NON TERMINAIL THREAD
            data = s.readline().decode() # DECODIFICA DEL MESSAGGIO PASSATO DALLA PORTA
            print("Termosifone") 
            messaggio = [space for space in data.split(';')] # SPLIT DEL MESSAGGIO DECODIFICATO
            qTerm.put(messaggio) # INVIO MESSAGGIO ALLA CODA TERMOFONE
            print(messaggio)
            time.sleep(0.01)

class Read_Microbit_Ambiente(threading.Thread): # CLASSE THREAD PER MICROBIT AMBIENTE
    def _init_(self):
        threading.Thread._init_(self)
        self._running = True

    def terminate(self): # FUZIONE CHE TERMINA IL THREAD
        self._running = False

    def run(self): # FUNZIONE CHE PARTE ALLA CREAZIONE DEL THREAD
        #serial config
        port = "COM5"
        s = serial.Serial(port) # AVVIA IL COLLEGAMMENTO CON LA PORTA SERIALE PASSAT TRA PARAMETRI
        s.baudrate = 115200 # SETTAGGIO NUMERO DI BIT INVIATI
        self._running = True
        while self._running: # FINO A CHE NON TERMINAIL THREAD
            data = s.readline().decode() # DECODIFICA DEL MESSAGGIO PASSATO DALLA PORTA
            messaggio = [space for space in data.split(';')] # SPLIT DEL MESSAGGIO DECODIFICATO
            print("Ambiente")
            qAmb.put(messaggio) # INVIO MESSAGGIO ALLA CODA AMBIENTE
            print(messaggio)
            time.sleep(0.01)

running = True
rmt = Read_Microbit_Termosifone() # CREAZIONE THREAD TERMOSIFONE
rma = Read_Microbit_Ambiente() # CREAZIONE THREAD AMBIENTE
rma.start()
rmt.start()
while running: # FINO ALLA CHIUSURA DEL PROGRAMMA
    messaggioAmb = qAmb.get() # INVIO MESSAGGIO DELLA CODA AMBIENTE
    print(messaggioAmb)
    print("####################")
    messaggioTerm = qTerm.get() # INVIO MESSAGGIO DELLA CODA TERMOSIFONE
    print(messaggioTerm)
    dataOra = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())) # DATA E ORA ATTUALE
    data = (messaggioTerm[0], messaggioTerm[1], messaggioTerm[2], messaggioAmb[0], dataOra) 
    addData(dataFile, data) # AGGIUNTA DATI A FILE CSV
rma.terminate()
rmt.terminate()
rmt.join()
rma.join()