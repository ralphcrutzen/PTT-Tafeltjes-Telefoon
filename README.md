# PTT Tafeltjes Telefoon (afgekort "PTT")
Verbind een T65 telefoon met een Raspberry Pi. Het gebruikte model is een Raspberry Pi 3 Model B. Besturingssysteem: Raspbian Jessie Lite.

Neem de hoorn op en kies met de draaischijf welk tafeltje je wil oefenen. Met de knop rechts onder de draaischijf (de aardtoets) oefen je alle tafeltjes door elkaar. Vervolgens hoor je minstens 10 sommen. Voer de uitkomst in via de draaischijf. Je hoort of het antwoord goed of fout is. Wanneer je een som fout beantwoord, komt hij op een ander moment weer terug, totdat het antwoord goed is. Som niet goed verstaan? Met de aardtoets wordt de opgave nog eens herhaald. Het oefenen stopt door de hoorn neer te leggen en begint opnieuw door de hoorn op te nemen.

## Aansluitingen

### Draaischijf

De contacten van de draaischijf en de knoppen onder de hoorn zijn in de telefoon met elkaar verbonden. Om het script toch het verschil tussen het draaien aan de schijf en het oppakken van de hoorn te kunnen laten detecteren, moeten er bij de draaischijf enkele verbindingen worden gewijzigd.

![draaischijf](https://github.com/ralphcrutzen/PTT-Tafeltjes-Telefoon/blob/master/foto/PTT-draaischijf.jpg)

* De rode draad van de draaischijf loskoppelen van de telefoon en verbinden met GPIO25 op de RPi.
* De blauwe draad van de draaischijf loskoppelen van de telefoon en verbinden met Ground op de RPi.
* De gele draad van de draaischijf loskoppelen en verbinden met "Rd" van de telefoon.
* Een extra stukje draad gebruiken om "Bl" met "Rd" in de telefoon met elkaar te verbinden.

### Luidspreker

Gebruik een audio kabel met jackplug (knip bijvoorbeeld de kabel van een koptelefoon door).

![luidspreker](https://github.com/ralphcrutzen/PTT-Tafeltjes-Telefoon/blob/master/foto/PTT-luidspreker.jpg)

* Draad zonder mantel van de audiokabel naar de blauwe aansluiting (11) van de hoorn in de aansluitkamer.
* Rode of witte draad van de audiokabel naar de rode aansluiting (12) van de hoorn in de aansluitkamer.

De kleur van de draad in de audiokabel kan bij andere kabels verschillend zijn.

### Aardknop en hoornknoppen

![aardknop-hoornknoppen](https://github.com/ralphcrutzen/PTT-Tafeltjes-Telefoon/blob/master/foto/PTT-hoornknoppen-aardknop.jpg)

* Rode aansluiting (1) van de aansluitkamer naar Ground op de RPi.
* Groene aansluiting (2) van de aansluitkamer naar GPIO23 op de RPi. (Aardtoets)
* Blauwe aansluiting (3) van de aansluitkamer naar GPIO24 op de RPi. (Hoornknoppen)

## Software installeren

* Plaats *t65.py* en de map *audio* in */home/pi/t65*.
* Om het programma automatisch uit te voeren wanneer de Raspberry Pi opstart, voeg je de volgende regel toe aan */etc/rc.local*, direct boven de regel ```exit 0```:
```
sudo amixer sset PCM,0 100% && cd /home/pi/t65 && python t65.py &
```

## Links

Oorspronkelijk idee: https://github.com/tammojan/sommentelefoon

PTT schema T65 toestellen: https://dutchtelecom.files.wordpress.com/2016/05/ptt_schema_t65_toestellen_1974-1987.pdf

Overzicht GPIO pinnen Raspberry Pi 3B: http://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Layout-Model-B-Plus-rotated-2700x900.png

Detecteren of een knop is ingedrukt: http://razzpisampler.oreilly.com/ch07.html

Interrupts: http://raspi.tv/2014/rpi-gpio-update-and-detecting-both-rising-and-falling-edges

Herstarten van het huidige Python programma: https://www.daniweb.com/programming/software-development/code/260268/restart-your-python-program

## Raspberry Pi Zero

Het is me ook gelukt om een Raspberry Pi Zero in de telefoon in te bouwen. De enige kabel die dan nog uit de telefoon komt, is de usb kabel. Ik heb de volgende dingen gedaan:

* Een Wifi dongle aangesloten en de volgende handleiding gebruikt om ssh toegang tot de Pi Zero te krijgen: https://davidmaitland.me/2015/12/raspberry-pi-zero-headless-setup/
* De Pi Zero geschikt maken om analoge audio af te spelen. Hiervoor heb ik de volgende handleiding gebruikt: https://learn.adafruit.com/adding-basic-audio-ouput-to-raspberry-pi-zero?view=all#overview. Ik heb "Option 2. Manually Assigning PWM pins" gevolgd. Omdat de audio mono is, heb ik deze handleiding alleen voor GPIO13 toegepast.
* De twee weerstanden en de twee condensatoren heb ik op een "Breakout Pi Zero" printplaatje gesoldeerd: https://www.abelectronics.co.uk/p/68/Breakout-Pi-Zero.
* De bellen, inclusief de spoel, het volumewieltje en de koperkleurige grondplaat waarop deze bevestigd zijn, uit de T65 verwijderd. Hiervoor heb ik de twee metalen strips die in de printplaat op de bodem vast zitten, doorgeknipt. De usb kabel komt naar buiten door het gat waar voorheen het volumewieltje zat.
* De 5 kabels van de draaischijf, aardknop en hoornknoppen heb ik niet meer in de aansluitkamer vastgemaakt, maar aan dezelfde schroeven in de binnenkant van de telefoon. Hiervoor moet je wel eerst de doorzichtige kap van de hoorknoppen losmaken.

## To do

* Het geluid klinkt veel te zacht met een Pi Zero. Uitzoeken of het nog harder kan. Wellicht door, naast GPIO13, ook GPIO18 te gebruiken?
