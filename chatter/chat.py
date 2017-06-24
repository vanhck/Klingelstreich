#!/usr/bin/python3

"""
Repräsentiert ein Chat-Objekt.
Attribute:

    id        --      einmalige, zur Identifikation benötigte, Chat-ID
    typ       --      Art des Chats, entweder "private", "group", "supergroup" oder "channel"
    titel     --      Titel von Gruppen, Suppergruppen und Kanälen, 'None' falls kein Titel vorhanden
"""

class Chat(object):

    def __init__(self, chat):
        self.id = chat["id"]
        self.typ = chat["type"]

        try:
            self.titel = chat["title"]
        except KeyError:
            self.titel = None
