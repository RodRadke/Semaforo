#!/bin/bash

python3 /home/pi/vision/tiempo_semaforico.py &

sleep 300

python3 /home/pi/vision/camara.py &
