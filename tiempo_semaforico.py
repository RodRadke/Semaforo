#!/usr/bin/env python3
#coding: utf-8
import numpy as np
import cv2
import datetime
import time
import os
import RPi.GPIO as io
import os.path
import time

pin = 40
io.setmode(io.BOARD)
io.setwarnings(False)
io.setup(pin,io.IN)

pasoc = 0
pasof = 0
sumara = 0
sumare = 0
tiempo = 0
segun_comi = 0
segun_fin = 0
pase = 0

while True:

    if io.input(pin) == True:  
        sumare += 1

        if sumare > 50000:
            sumare = 0

            if pase == 1:
                if pasoc == 0:

                    pasoc = 1
                    pasof = 0
                    horacomienzo = time.strftime("%H:%M:%S") # Hora actual en formato de 24 horas                    
                    segun_comi1 = int(horacomienzo [0:2]) * 60 * 60
                    segun_comi2 = int(horacomienzo [3:5]) * 60 
                    segun_comi3 = int(horacomienzo [6:8])
                    segun_comi = (segun_comi1 + segun_comi2 + segun_comi3)                
                                  
                    print ('Encendido...', horacomienzo)
                        
    else:

        sumara += 1
        
        if sumara > 40000:                 
            sumara = 0

            if pase == 1:
                if pasof == 0:

                    pasof = 1
                    pasoc = 0
                    horafin = time.strftime("%H:%M:%S") # Hora actual en formato de 24 horas             
                    segun_fin1 = int(horafin [0:2]) * 60 * 60
                    segun_fin2 = int(horafin [3:5]) * 60 
                    segun_fin3 = int(horafin [6:8])
                    segun_fin = (segun_fin1 + segun_fin2 + segun_fin3)                    
                    tiempo = segun_fin - segun_comi

                    if tiempo < 0:
                        tiempo = tiempo + 86400
                    
                    if tiempo < 120:
                        if tiempo > 10:                        
                            print ('Apagado...', horafin)
                            print ('Tiempo Semáforo en Rojo...', tiempo)

                            file = open("/home/pi/vision/duracion.txt", "w")
                            file. write(str((tiempo)))
                            file. close()

                            time.sleep(300)

            else:
                pase = 1
