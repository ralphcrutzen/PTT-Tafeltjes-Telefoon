#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys
import os
import time
import random
import pygame

SCHIJFPIN = 18
AARDPIN = 23
HOORNPIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(SCHIJFPIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(HOORNPIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(AARDPIN, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Laag als ingedruk!!!

pygame.mixer.init()


def speel(bestand):
    pygame.mixer.music.load(bestand)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


def speelSom(getal1, getal2):
    print "Wat is", getal1, "x", getal2,"?"
    speel("audio/" + str(getal1) + ".mp3")
    speel("audio/keer.mp3")
    speel("audio/" + str(getal2) + ".mp3")
    speel("audio/is.mp3")


def getNummer():
    nPulsen = 0
    # Wacht op draaischijf / knop
    schijfContact = GPIO.input(SCHIJFPIN)
    aardContact = GPIO.input(AARDPIN) # Laag als ingedrukt!!!
    while schijfContact == False and aardContact == True:
        schijfContact = GPIO.input(SCHIJFPIN)
        aardContact = GPIO.input(AARDPIN)

    # Aardtoets ingedrukt
    if aardContact == False:
        return -1

    # Afhandelen van pulsen
    klaar = False
    while klaar == False and schijfContact == True:
        nPulsen = nPulsen + 1
        startTijd = time.time()
        time.sleep(0.1)
        schijfContact = GPIO.input(SCHIJFPIN)

        # Controleer tijd tussen twee pulsen
        while klaar == False and schijfContact == False:
            if time.time() - startTijd >= 0.2:
                klaar = True
            schijfContact = GPIO.input(SCHIJFPIN)

    return nPulsen % 10


def hoornCallback(channel):
    print "Hoorn!", channel
    # herstart het hele script
    GPIO.cleanup()
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Gebruik een interrupt voor de hoorn,
# omdat deze op elk moment kan worden neergelegd
GPIO.add_event_detect(HOORNPIN, GPIO.BOTH, callback = hoornCallback)

while True:
    try:
        # Wacht op hoorn
        print "Pak de hoorn op!"
        hoornContact = GPIO.input(HOORNPIN)
        while hoornContact == True:
            hoornContact = GPIO.input(HOORNPIN)
        time.sleep (2)

        # Welk tafeltje oefenen?
        print "Welk tafeltje?"
        speel("audio/welk.mp3")
        tafeltje = getNummer()

        for som in range(10):
            # Bepaal opgave
            getal1 = random.randint(1,10)
            if tafeltje == -1:
                getal2 = random.randint(1,10)
            elif tafeltje == 0:
                getal2 = 10
            else:
                getal2 = tafeltje
            uitkomst = getal1 * getal2
            nCijfers = len(str(uitkomst))

            speelSom(getal1, getal2)
            huidigCijfer = 0
            antwoord = ""

            # Wacht op antwoord
            while huidigCijfer < nCijfers:
                nummer = getNummer()
                if nummer > -1: # aan schijf gedraaid
                    antwoord = antwoord + str(nummer)
                    huidigCijfer = huidigCijfer + 1
                else: # aardtoets ingedrukt
                    speelSom(getal1, getal2)
                    huidigCijfer = 0
                    antwoord = ""
            print antwoord

            # Controleer antwoord
            if int(antwoord) == uitkomst:
                print "Goed zo!"
                speel("audio/" + str(antwoord) + ".mp3")
                speel("audio/goed.mp3")
            else:
                print "Jammer, de juiste uitkomst is", uitkomst
                speel("audio/fout.mp3")
                speel("audio/" + str(uitkomst) + ".mp3")
            print
            time.sleep(1)
    except KeyboardInterrupt: # Ctrl+C
        GPIO.cleanup()
