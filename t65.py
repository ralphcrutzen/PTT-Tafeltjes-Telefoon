#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import random
import pygame

SCHIJFPIN = 18
AARDPIN = 21
HOORNPIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(SCHIJFPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(HOORNPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(AARDPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Laag als ingedruk!!!

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
    # Wacht op draaischijf en knop
    schijfContact = GPIO.input(SCHIJFPIN)
    aardContact = GPIO.input(AARDPIN)
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


while True:
    # Bepaal opgave
    getal1 = random.randint(1,10)
    getal2 = random.randint(1,10)
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
        speel("audio/goed.mp3")
    else:
        print "Jammer, de juiste uitkomst is", uitkomst
        speel("audio/fout.mp3")
    print
    time.sleep(1)
