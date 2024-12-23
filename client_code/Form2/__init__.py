from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.js

class Form2(Form2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Prüfe ggf. URL-Parameter (z.B. Injection über die URL)
        self.handle_url_parameters()

    def handle_url_parameters(self):
        """Über die URL übergebene Parameter abfragen"""
        url = anvil.js.window.location.href
        params = anvil.js.window.location.search  # z.B. '?AccountNo=1 OR 1=1'

        if params:
            query = {}
            # "?AccountNo=1 OR 1=1" -> Remove '?' und split
            pairs = params[1:].split("&")
            for pair in pairs:
                key, value = pair.split("=")
                query[key] = value

            # Wenn 'AccountNo' übergeben wurde
            if "AccountNo" in query:
                account_no = query["AccountNo"]

                # Evtl. einfache Prüfung auf gefährliche Zeichen
                if "UNION" in account_no.upper() or ";" in account_no:
                    self.label_info.text = "Unsichere Eingabe erkannt und blockiert!"
                else:
                    # Da Level2 ALLE Kontostände anzeigen soll:
                    # Rufe Server-Funktion auf und hole alle Balances
                    all_balances = anvil.server.call('get_all_balances')
                    if isinstance(all_balances, list):
                        anzeigen = [f"Account: {acc_no}, Kontostand: {bal}€"
                                    for acc_no, bal in all_balances]
                        self.label_info.text = "\n".join(anzeigen)
                    else:
                        self.label_info.text = f"Fehler: {all_balances}"
            else:
                self.label_info.text = "Kein 'AccountNo' in den Parametern gefunden."
        else:
            self.label_info.text = "Keine URL-Parameter vorhanden."

    def button_alle_anzeigen_click(self, **event_args):
        """Button zum Anzeigen aller Kontostände (ohne URL-Parameter)"""
        all_balances = anvil.server.call('get_all_balances')
        if isinstance(all_balances, list):
            anzeigen = [f"Account: {acc_no}, Kontostand: {bal}€"
                        for acc_no, bal in all_balances]
            self.label_info.text = "\n".join(anzeigen)
        else:
            self.label_info.text = f"Fehler: {all_balances}"
