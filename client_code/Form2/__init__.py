from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.js
from anvil.js.window import URLSearchParams

class Form2(Form2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # 1) Parameter aus der URL holen
        search_params = URLSearchParams(anvil.js.window.location.search)
        account_no_str = search_params.get("AccountNo")

        # 2) Prüfen: ist AccountNo=0 angegeben?
        if account_no_str == "0":
            # 3) Dann rufe z.B. Server-Funktion auf
            balance = anvil.server.call('get_balance', 0)

            # 4) Falls ein Kontostand gefunden wurde, anzeigen
            if balance is not None:
                alert(f"Kontostand für Account 0: {balance} EUR")
            else:
                alert("Kein Account mit Nummer 0 gefunden.")
        else:
            # Falls kein Parameter oder anderer Wert, passiert nichts
            pass
