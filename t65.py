import RPi.GPIO as GPIO
import time
import random
import pygame

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.mixer.init()


def speel(bestand):
    pygame.mixer.music.load(bestand)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


def getNummer():
    nPulsen = 0
    # Wacht op draaischijf
    schijfContact = GPIO.input(18)
    while schijfContact == False:
        schijfContact = GPIO.input(18)

    # Afhandelen van pulsen
    klaar = False
    while klaar == False and schijfContact == True:
        nPulsen = nPulsen + 1
        startTijd = time.time()
        time.sleep(0.1)
        schijfContact = GPIO.input(18)

        # Controleer tijd tussen twee pulsen
        while klaar == False and schijfContact == False:
            if time.time() - startTijd >= 0.2:
                klaar = True
            schijfContact = GPIO.input(18)

    if klaar == True:
        return nPulsen % 10


while True:
    # Bepaal opgave
    getal1 = random.randint(1,10)
    getal2 = random.randint(1,10)
    uitkomst = getal1 * getal2
    nCijfers = len(str(uitkomst))
    print "Wat is", getal1, "x", getal2,"?"
    speel("audio/" + str(getal1) + ".mp3")
    speel("audio/keer.mp3")
    speel("audio/" + str(getal2) + ".mp3")
    speel("audio/is.mp3")

    huidigCijfer = 0
    antwoord = ""

    # Wacht op antwoord
    while huidigCijfer < nCijfers:
        nummer = getNummer()
        antwoord = antwoord + str(nummer)
        huidigCijfer = huidigCijfer + 1
    print antwoord

    # Controleer antwoord
    if int(antwoord) == uitkomst:
        print "Goed zo!"
        speel("audio/goed.mp3")
    else:
        print "Jammer, de juiste uitkomst is", uitkomst
        speel("audio/fout.mp3")
    print
