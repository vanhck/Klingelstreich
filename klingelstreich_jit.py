from datetime import time
from config import OAUTH, ID

from chatter.apiHandler import *
from resources.Order import Order
from texte import *

class Chatbot_JIT(TelegramBot):

    def aktivieren(self, order):

        self.gehe_online()
        print("Bot ist aktiviert")

        id = ID

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

        nachrichten = self.hole_updates()

        while (True):
            time.sleep(1)

            nachrichten = self.hole_updates()

            for nachricht in nachrichten:
                self.reagiere(nachricht)

        print("Bot wird deaktiviert")

    def confirm(self, antwort):
        self.sende_nachricht("Sehr gut!", antwort.sender.id)

    def deny(self, antwort):
        self.sende_nachricht('Okay. Willst du das Paket stattdessen bei einem Nachbarn ablegen lassen?',
                             antwort.sender.id)

        antwort = 0

        while not antwort:

            nachrichten = self.hole_updates()
            if len(nachrichten) > 0:
                antwort = nachrichten[0]

        if antwort.inhalt in JA:
            Order.Lieferwunsch = 1
            self.sende_nachricht("Alles klar!", antwort.sender.id)
        else:
            Order.Lieferwunsch = 2
            self.sende_nachricht("Okay. Das Paket wird in der, deiner Wohnung am nähesten, Packstation abgelegt.",
                                 antwort.sender.id)
        self.sende_nachricht("Falls du noch irgendwelche Fragen hast, kannst du mir jederzeit schreiben.",
                             antwort.sender.id)

Chatbot_JIT(OAUTH).aktivieren()