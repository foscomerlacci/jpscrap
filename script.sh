#! /bin/bash

# cd /home/utente/PycharmProjects/Test/jpscrap
#for i in {1..1000}
##while(true)
##do
##    python3 subito.py
##   python3 kitlavoro.py
##    python3 iprogrammatori.py
##    sleep 30m
##done

cd /home/pi/PycharmProjects/jpscrap/ && fuser -k test.sqlite
cd /home/pi/PycharmProjects/jpscrap/ && python3 subito.py
sleep 1m
cd /home/pi/PycharmProjects/jpscrap/ && fuser -k test.sqlite
cd /home/pi/PycharmProjects/jpscrap/ && python3 kitlavoro.py
sleep 1m
cd /home/pi/PycharmProjects/jpscrap/ && fuser -k test.sqlite
cd /home/pi/PycharmProjects/jpscrap/ && python3 iprogrammatori.py
