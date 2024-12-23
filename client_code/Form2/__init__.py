from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.js

class Form2(Form2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Prüfe gleich beim Start, ob Parameter in der URL vorhanden sind
        self.handle_url_parameters()

    def handle_url_parameters(self):
        """
        Liest die URL-Parameter (z.B. "?AccountNo=0 OR 1=1") und ruft
        den unsicheren Server-Call auf.
        """
        params = anvil.js.window.location.search  # z.B. "?AccountNo=0%20OR%201=1"
        if params:
            # params beginnt mit '?', also schneiden wir das ab und splitten nach '&'
            pairs = params[1:].split("&")
            query = {}
            for pair in pairs:
                key, value = pair.split("=")
                # Bei Bedarf könnte man URL-decodieren: 
                #   value = anvil.js.window.decodeURIComponent(value)
                query[key] = value

            if "AccountNo" in query:
                account_no = query["AccountNo"]  # "0 OR 1=1" (URL-encodet: "0%20OR%201=1")
                
                # Rufe jetzt die unsichere Funktion auf
                result = anvil.server.call('get_all_balances_insecure', account_no)
                self.textbalances.text = result
            else:
                self.textbalances.text = "Parameter 'AccountNo' fehlt."
        else:
            self.textbalances.text = "Keine URL-Parameter gefunden."
