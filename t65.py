import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

klaar = True

while True:
    if klaar == True:
        getal1 = random.randint(1,10)
        getal2 = random.randint(1,10)
        uitkomst = getal1 * getal2
        nCijfers = len(str(uitkomst))
        print "Wat is", getal1, "x", getal2,"?"
        huidigCijfer = 0
        antwoord = ""

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

        # Controleer uitkomst
        if klaar == True:
            nPulsen = nPulsen % 10 # 10 pulsen is het cijfer 0
            antwoord = antwoord + str(nPulsen)
            huidigCijfer = huidigCijfer + 1
            if huidigCijfer == nCijfers:
                print antwoord
                if int(antwoord) == uitkomst:
                    print "Goed zo!"
                else:
                    print "Jammer, de juiste uitkomst is", uitkomst
                print
            else:
                klaar = False
