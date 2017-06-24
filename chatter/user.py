#!usr/bin/python3

"""
Repräsentiert ein User-Objekt
Attribute:

    id          --  einmalige, zur Identifikation benötigte, ID
    vorname     --  Vorname des Users
    nachname    --  Nachname des Users, 'None' falls nicht vorhanden
    username    --  Username des Users, 'None' falls nicht vorhanden
"""

class User(object):
    # represents a user
    # attributes
    #   id      --  unique identifier for the user
    #   vorname  --  first name of the user
    #   nachname   --  last name of the user
    #   status   --    at home or not at time of delivery

    def __init__(self, user):
        self.id = user["id"]
        self.vorname = user["first_name"]
        self.status = 0
        try:
            self.nachname = user["last_name"]
        except KeyError:
            self.nachname = None
        try:
            self.username = user["username"]
        except KeyError:
            self.username = None
