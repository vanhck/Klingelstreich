#!usr/bin/python3

"""
Eine Unterklasse von TelegramBot, die die Funktionalität um eine einfache Spracherkennung erweitert.
Objekte dieser Klasse können auf verschiedene Wörter/Sätze  reagieren und senden entsprechende Antworten an den Chat
"""
import time

import config
from chatter.apiHandler import TelegramBot
from resources.Order import Order
from texte import *

import random

class Chatbot_EarlySupport(TelegramBot):

    order = None

    # Funktion aktivieren
    # enthält den main-loop des Bots. Die Methode setzt zunächst das online-Attribut. Danach wird alle 1sek
    # nach Updates gefragt. Auf jede erhaltene Nachricht wird konsekutiv die Methode reagiere() aufgerufen.

    def aktivieren(self, new_order):

        global user, date, place

        order = new_order

        self.gehe_online()
        print("Bot ist aktiviert")

        id = config.ID

        self.sende_nachricht(INTRODUCTION, id)
        time.sleep(1)
        self.sende_nachricht(INITIALIZE_CONVO + order.giveDateAsString(), id)
        time.sleep(1)
        self.sende_nachricht(ZUHAUSE, id)

        antwort = 0

        while not antwort:
            nachrichten = self.hole_updates()
            if len(nachrichten) > 0:
                antwort = nachrichten[0]

        if antwort.inhalt in JA:
            self.confirm(antwort)
        else:
            self.deny(antwort)

        i = 0
        while(i < 3):
            nachrichten = self.hole_updates()
            for nachricht in nachrichten:
                self.reagiere(nachricht)
                i += 1
            time.sleep(1)

        if order.Lieferwunsch == 0:
            time.sleep(3)
            self.sende_nachricht("Das Warten hat ein Ende! Dein Paket wird in den nächsten 30min bei dir sein.", id)
            time.sleep(1)
            self.sende_nachricht("Bist du zu Hause, um die Lieferung in Empfang zu nehmen?", id)

            antwort = 0

            while not antwort:

                nachrichten = self.hole_updates()
                if len(nachrichten) > 0:
                    antwort = nachrichten[0]

            if antwort.inhalt in JA:
                self.confirm(antwort)
            else:
                self.deny(antwort)

        time.sleep(3)

        if order.Lieferwunsch == 0:
            self.sende_nachricht("Dein Paket ist zu Hause angekommen.", id)
        elif order.Lieferwunsch == 1:
            self.sende_nachricht("Dein Nachbar hat dein Packet für dich entgegen genommen.", id)
        elif order.Lieferwunsch == 2:
            self.sende_nachricht("Dein Packet wurde in der Paketstation ABC hinterlegt.", id)
        else:
            print("OH GOD NO")

        order.Lieferstatus = 2

        print("Bot wird deaktiviert")

    # Funktion reagiere()
    # Funktion steuert, wie der Bot auf eine Nachricht reagiert.
    # Parameter:
    #   nachricht   --  Nachricht-Objekt, die Nachricht auf die reagiert werden soll

    def reagiere(self, nachricht):
        name = nachricht.sender.vorname
        chat = nachricht.chat.id


        ' Frage: wann kommt mein Paket?'

        if "wann" in nachricht.inhalt and "paket" in nachricht.inhalt:
            self.sende_nachricht("Die Auslieferung deines Pakets is geplant für den " + Order().giveDateAsString(), nachricht.chat.id)
            time.sleep(1)
            self.sende_nachricht("Bist du damit einverstanden?", nachricht.chat.id)

            antwort = 0

            while not antwort:

                nachrichten = self.hole_updates()
                if len(nachrichten) > 0:
                    antwort = nachrichten[0]

            if antwort.inhalt in JA:
                self.confirm(nachricht)
            else:
                self.deny(nachricht)


        ' Frage: wo ist mein Paket gerade'

        if "wo" in nachricht.inhalt and "paket" in nachricht.inhalt:
            self.sende_nachricht("Dein Paket ist noch in der Lieferzentrale.", nachricht.chat.id)


        ' Frage: Ich bin nicht zuhause'

        if "nicht" in nachricht.inhalt and ("zuhause" in nachricht.inhalt or "zu hause" in nachricht.inhalt):
            self.deny(nachricht)

        if "hilfe" in nachricht.inhalt or "help" in nachricht.inhalt:
            self.sende_nachricht("Ich kann dir beantworten, wo dein Paket ist oder wann es ankommt. Bitte sage mir, falls du zur Zustellzeit nicht zu Hause bist. Falls du Fragen hast welche ich nicht beantworten kann, melde dich unter folgender Nummer: 0800 XXXXXX.", nachricht.sender.id)

    def confirm(self, nachricht):
        Chatbot_EarlySupport.Lieferwunsch = 0
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

        if antwort.inhalt in JA:
            Order.Lieferwunsch = 1
            self.sende_nachricht("Alles klar!", nachricht.sender.id)
        else:
            Order.Lieferwunsch = 2
            self.sende_nachricht("Okay. Das Paket wird in der, deiner Wohnung am nähesten, Packstation abgelegt.", nachricht.sender.id)
        self.sende_nachricht("Falls du noch irgendwelche Fragen hast, kannst du mir jederzeit schreiben.",
                                 nachricht.sender.id)


boty = Chatbot_EarlySupport(config.OAUTH)
boty.aktivieren(Order())
