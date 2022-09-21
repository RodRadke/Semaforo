#!/usr/bin/env python3
#coding: utf-8
import numpy as np
import cv2
import datetime
import time
import os
import RPi.GPIO as io
import os.path, time
import shutil

fileNameOutput = ""
duracion = 0
num_frames_gra = 0
pin = 40
io.setmode(io.BOARD)
io.setwarnings(False)
io.setup(pin,io.IN)

# Abrir el archivo de Condiguración
f = open("/home/pi/vision/config.txt", "r")
while(True):    
    linea = f.readline()
    ipcam = (linea [0:15]).strip()    
    usuario_cam = (linea [15:22]).strip()
    password_cam = (linea [22:30]).strip()
    dato1 = linea [30:34]
    dato2 = linea [34:38]
    dato3 = linea [38:42]
    dato4 = linea [42:46]
    dato11 = linea [46:50]
    dato22 = linea [50:54]
    dato33 = linea [54:58]
    dato44 = linea [58:62]
    nombre_camara = (linea [62:70]).strip()
    hdesde = linea [70:78]
    hhasta = linea [78:86]
    desdemili = int(hdesde [0:2] + hdesde [3:5])
    hastamili = int(hhasta [0:2] + hhasta [3:5]) 
    break    
    if not linea:
        break    
f.close()

# Abrir Tiempo de Duración de Semáforo
g = open("/home/pi/vision/duracion.txt", "r")
while(True):    
    duracion = int(g.readline())    
    break    
    if not duracion:
        break    
g.close()
    
# Nombre de la entrada de Video en Vivo
fileName = "rtsp://" + usuario_cam + ":" + password_cam + "@" + ipcam + ":554/cam/realmonitor?channel=1&subtype=0"
    
# Inicialice la secuencia de video, el puntero para generar el archivo de video y dimensiones del marco
videoStream = cv2.VideoCapture(fileName, cv2.CAP_FFMPEG)
video_width = int(videoStream.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(videoStream.get(cv2.CAP_PROP_FRAME_HEIGHT))
fecha_creacion = ("created: %s" % time.ctime(os.path.getctime("/home/pi/vision/config.txt")))
fecha_creacion_duracion = ("created: %s" % time.ctime(os.path.getctime("/home/pi/vision/duracion.txt")))

# PROPÓSITO: Inicializar la grabadora de video con la ruta de salida de video y el mismo número
# de fps, ancho y alto como el video de origen
# PARÁMETROS: Ancho del video de origen, Alto del video de origen, la transmisión de video
# DEVOLUCION: el escritor de video inicializado
def initializeVideoWriter(video_width, video_height, videoStream):
    # Obteniendo los fps del video fuente
    sourceVideofps = videoStream.get(cv2.CAP_PROP_FPS)
    # Inicializar nuestro escritor de video
    fourcc = cv2.VideoWriter_fourcc(*'mp4')
    return cv2.VideoWriter(fileNameOutput, fourcc, sourceVideofps, (video_width, video_height), True)
# Genero una ventana que anuncia que el Sistema entró en Trabajo
cv2.imshow ('TRABAJANDO......', num_frames_gra)
pase = 0
# Recorrer los fotogramas del video entrante
while True: 
    isadentro = False
    # Controlar el Archivo de Configuración no haya cambiado
    fecha_nueva = ("created: %s" % time.ctime(os.path.getctime("/home/pi/vision/config.txt")))
    if fecha_nueva != fecha_creacion:        
        fecha_creacion = fecha_nueva        
        # Cargar el Archivo de Configuración
        f = open("/home/pi/vision/config.txt", "r")
        while(True):    
            linea = f.readline()
            ipcam = (linea [0:15]).strip()    
            usuario_cam = (linea [15:22]).strip()
            password_cam = (linea [22:30]).strip()
            dato1 = linea [30:34]
            dato2 = linea [34:38]
            dato3 = linea [38:42]
            dato4 = linea [42:46]
            dato11 = linea [46:50]
            dato22 = linea [50:54]
            dato33 = linea [54:58]
            dato44 = linea [58:62]
            nombre_camara = (linea [62:70]).strip()
            hdesde = linea [70:78]
            hhasta = linea [78:86]
            desdemili = int(hdesde [0:2] + hdesde [3:5])
            hastamili = int(hhasta [0:2] + hhasta [3:5]) 
            break    
            if not linea:
                break    
        f.close()
    # Controlar el Archivo de Tiempo Semafórico no haya cambiado
    fecha_nueva_du = ("created: %s" % time.ctime(os.path.getctime("/home/pi/vision/config.txt")))
    if fecha_nueva_du != fecha_creacion_duracion:        
        fecha_creacion_duracion = fecha_nueva_du        
        # Cargar el Archivo de Configuración
        g = open("/home/pi/vision/duracion.txt", "r")
        while(True):    
            duracion = int(g.readline())    
            break    
            if not duracion:
                break    
        g.close()
    # Controlar el Rango de Horarios 
    ahora = time.strftime("%H:%M:%S") # Hora actual en formato de 24 horas 
    ahoramili = int(ahora [0:2] + ahora [3:5])
    # Defino si está dentro de los horarios indicados para grabar o no
    if ahoramili >= desdemili:
        if ahoramili <= hastamili:            
            isadentro = True  
    if(isadentro):
        if pase == 0:            
            if io.input(pin) == False:
                pase = 1
        else:
            # Leer el fotograma de la cámara    
            (grabbed, frame) = videoStream.read()                    
            if io.input(pin) == True: # Comienza a grabar el video cuando recibe la señal del Relay          
                # Si el escritor de video no se ha inicializado, inicialícelo                
                if (num_frames_gra) == 0:                    
                    # Grabar en Micro SD de Raspberry
                    fileNameOutput = "/home/pi/vision/Videos/video_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".mp4"                                
                    writer = initializeVideoWriter(video_width, video_height, videoStream)  
                    writer.write(frame)
                    num_frames_gra += 1
                else:
                    writer.write(frame)
                    num_frames_gra += 1
            else: # Cierra el video al no recibir más la señal del Relay                
                if num_frames_gra != 0:                    
                    if num_frames_gra <= ((duracion * 10) - 10):                        
                        writer.write(frame)
                        num_frames_gra += 1
                    else:
                        writer.release()
                        num_frames_gra = 0
    else:
        pase = 0
        # Leer el fotograma de la cámara    
        (grabbed, frame) = videoStream.read()
        # Cambio el tamaño de la imagen para que se vea toda en pantalla cuando procesa
        #imagenmodificada = cv2.resize(frame, (1080,540))
        #cv2.imshow('Imagen...', imagenmodificada)        
        if num_frames_gra != 0:                    
            if num_frames_gra <= ((duracion * 10) - 10):                
                writer.write(frame)
                num_frames_gra += 1
            else:
                writer.release()
                num_frames_gra = 0    
        # Controlar la Hora para comenzar a Copiar los Videos a la Memoria USB
        ahoraco = time.strftime("%H:%M:%S") # Hora actual en formato de 24 horas 
        ahoramilico = int(ahoraco [0:2] + ahoraco [3:5])
        if ahoramilico == 30:            
            if io.input(pin) == False:        
                if (shutil.disk_usage("/home/pi/vision/Videos/").used) < (shutil.disk_usage("/media/pi/USB/").free):                    
                    initial_count = 0
                    dir = "/home/pi/vision/Videos/"
                    for path in os.listdir(dir):
                        if os.path.isfile(os.path.join(dir, path)):
                            initial_count += 1
                            if initial_count != 0:
                                # Copiar los Videos a la Memoria USB
                                if os.path.isdir('/media/pi/USB/' + nombre_camara + '/'):
                                    print('La carpeta existe.')
                                # Si no existe la carpeta, la creo
                                else:
                                    print('La carpeta No existe y entonces la creo.')
                                    os.mkdir('/media/pi/USB/' + nombre_camara + '/')
                                # Copio los videos
                                file_source = '/home/pi/vision/Videos/'                                
                                file_destination = '/media/pi/USB/' + nombre_camara + '/'                                
                                get_files = os.listdir(file_source)                                 
                                # Recorro todos los archivos de la carpeta 
                                for g in get_files:
                                    shutil.move(file_source + g, file_destination)
        # Controlar la Hora para reiniciar la Raspberry así puede usarse sin problemas
        ahorarei1 = time.strftime("%H:%M:%S") # Hora actual en formato de 24 horas 
        ahoramilirei1 = int(ahorarei1 [0:2] + ahorarei1 [3:5])
        if ahoramilirei1 == 500:
            # Reiniciar la Raspeberry para normalizar todo el sistema
            os.system("sudo reboot")
