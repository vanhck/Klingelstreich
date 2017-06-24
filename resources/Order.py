from datetime import datetime
import locale


# fake enums -- Lieferstatus
IM_LIEFERZENTRUM = 0
IM_VAN = 1
AUSGELIEFERT = 2

# fake enums -- Lieferwunsch
ADRESSE = 0
NACHBAR = 1
PACKSTATION = 2


class Order(object):

    Lieferstatus = 0  # wo befindet sich das Paket?
    Lieferwunsch = 0  # wohin soll das Paket geliefert werden?

    def __init__(self):
        self.date = datetime.today()
        self.timeframe = [14, 17]
        self.address = "Rintheimer Straße 15"

    def giveDateAsString(self):
        locale.setlocale(locale.LC_ALL, "")
        return self.date.strftime("%d. %B %Y")

print(Order().giveDateAsString())
