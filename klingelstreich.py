#!usr/bin/python3

"""
Eine Unterklasse von TelegramBot, die die Funktionalität um eine einfache Spracherkennung erweitert.
Objekte dieser Klasse können auf verschiedene Wörter/Sätze  reagieren und senden entsprechende Antworten an den Chat
"""
import os
import random
import time
from datetime import datetime
import sys

import select

from chatter.apiHandler import TelegramBot
from texte import *
import config

__author__ = 'Tina Maria Stroessner'
__license__ = 'MIT'
__version__ = 'v1.0'


class Chatbot(TelegramBot):

    # Funktion aktivieren
    # enthält den main-loop des Bots. Die Methode setzt zunächst das online-Attribut. Danach wird alle 5sek
    # nach Updates gefragt. Auf jede erhaltene Nachricht wird konsekutiv die Methode reagiere() aufgerufen.

    imAuto = False;

    def aktivieren(self):
        global user, date, place
        date = "26. Juni zwischen 14:00 und 17:00 Uhr"
        palce = "Adresse"

        self.gehe_online()
        print("Bot ist aktiviert")

        nachricht = self.hole_updates()

        if len(nachricht) > 0:
            user = nachricht[0].sender
            id = user.id
        else:
            id = 273614685

        self.sende_nachricht(INITIALIZE_CONVO + date, id)
        time.sleep(1)
        self.sende_nachricht("Bist du an diesem Termin zu Hause, um die Lieferung entgegenzunehmen?", id)


        antwort = 0

        while not antwort:

            nachrichten = self.hole_updates()
            if len(nachrichten) > 0:
                antwort = nachrichten[0]

        if antwort in JA:
            self.confirm(antwort)
        else:
            self.deny(antwort)

        nachrichten = self.hole_updates()

        millis = int(round(time.time() * 1000))

        while(True):
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            for nachricht in nachrichten:
                self.reagiere(nachricht)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                break

        print("ende")



        print("Bot wird deaktiviert")

    # Funktion reagiere()
    # Funktion steuert, wie der Bot auf eine Nachricht reagiert.
    # Parameter:
    #   nachricht   --  Nachricht-Objekt, die Nachricht auf die reagiert werden soll

    def reagiere(self, nachricht):
        name = nachricht.sender.vorname
        chat = nachricht.chat.id


        ' Frage: wann kommt mein Paket?'

        if "wann" in nachricht:
            self.sende_nachricht("Die Auslieferung deines Pakets is geplänt für den" + date)
            time.sleep(1)
            self.sende_nachricht("Bist du damit einverstanden?")

            if self.hole_updates()[0] in JA:
                self.confirm(nachricht)
            else:
                self.deny(nachricht)


        ' Frage: wo ist mein Paket gerade'

        if "wo" in nachricht and "paket" in nachricht:
            if imAuto:
                self.sende_nachricht("Dein Paket befindet sich auf dem Weg zu dir.")
            else:
                self.sende_nachricht("Dein Paket ist noch in der Packstation.")


        '''
        begruessung_benutzt = [wort for wort in nachricht.inhalt.split() if wort in BEGRUESSUNG]
        verabschiedung_benutzt = [wort for wort in nachricht.inhalt.split() if wort in VERABSCHIEDUNG]

        if not len(Chatbot.antworten) == 0 and chat == Chatbot.antworten[0][1]:

            if Chatbot.antworten[0][0] == " wer?":
                Chatbot.antworten[0][0] = nachricht.inhalt + " wer?"

            self.sende_nachricht(Chatbot.antworten[0][0], Chatbot.antworten[0][1])
            del Chatbot.antworten[0]

        elif len(begruessung_benutzt) > 0:
            antwort = random.choice(BEGRUESSUNG) + ", " + name
            self.sende_nachricht(antwort, chat)
                
        elif len(verabschiedung_benutzt) > 0:
            antwort = random.choice(VERABSCHIEDUNG) + ", " + name
            self.sende_nachricht(antwort, chat)
            self.gehe_offline()

        elif nachricht.inhalt == "klopf klopf":
            self.sende_nachricht("Wer ist da?", chat)
            Chatbot.antworten.append([" wer?", chat])
            Chatbot.antworten.append(["Hahaha😂", chat])

        elif nachricht.inhalt in IDENTITAET:
            self.sende_nachricht("Ich heiße " + self.name + ". Ich bin ein Bot. Hilf mir dabei neue Sachen zu lernen.",
                                 chat)

        elif "uhr" in nachricht.inhalt:
            self.sende_nachricht("Es ist " + str(datetime.now().strftime("%H:%M") + " Uhr"), chat)

        elif nachricht.inhalt == "/start":
            self.sende_nachricht("Ich bin ein Bot. Chatte mit mir!", chat)

        # # # # # # # # # # # # # # # # # # # #
        # Schreibe hier deinen Code, um dem Bot noch mehr Wörter beizubringen

        elif nachricht.inhalt == "wie geht es dir?":
            self.sende_nachricht(random.choice(GEFUEHLS_ZUSTAND), chat)

        elif "warum" in nachricht.inhalt:
            self.sende_nachricht("Darum", chat)

        # # # # # # # # # # # # # # # # # # # #

        else:
            self.sende_nachricht("Du nuschelst", chat)

        '''

    def confirm(self, nachricht):
        user.status = 1
        self.sende_nachricht("Super! Dann wird dein Paket schon bald bei dir sein.", nachricht.sender.id)
        time.sleep(1)
        self.sende_nachricht("Falls du noch irgendwelche Fragen hast, kannst du mir jederzeit schreiben.", nachricht.sender.id)

    def deny(self, nachricht):
        self.sende_nachricht('Okay. Willst du das Paket stattdessen bei einem Nachbarn ablegen lassen?', nachricht.sender.id)

        antwort = 0

        while not antwort:

            nachrichten = self.hole_updates()
            if len(nachrichten) > 0:
                antwort = nachrichten[0]

        if antwort in JA:
            self.sende_nachricht("Alles klar!", nachricht.sender.id)
        else:
            self.sende_nachricht("Okay. Das Paket wird in der, deiner Wohnung am nähesten, Packstation abgelegt.", nachricht.sender.id)


boty = Chatbot(config.OAUTH)
boty.aktivieren()
