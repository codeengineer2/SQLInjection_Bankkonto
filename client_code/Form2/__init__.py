from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.js
from anvil.js.window import URLSearchParams

class Form2(Form2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # 1) Hash-Teil der URL abfragen
        full_hash_str = anvil.js.window.location.hash
        
        # Prüfen, ob überhaupt ein Hash existiert
        if not full_hash_str:
            self.textbalances.text = "Es befindet sich kein Hash in der URL."
            return
        
        # -> Normalerweise beginnt full_hash_str mit "#?"
        # Beispiel: "#?AccountNo=1000"
        # Prüfen, ob nach '#?' noch etwas folgt:
        if len(full_hash_str) <= 2:
            self.textbalances.text = "Keine Parameter nach '#?' gefunden."
            return
        
        # 2) Den Teil nach '#?' rausziehen
        #    "#?AccountNo=1000" -> "AccountNo=1000"
        param_str = full_hash_str[2:]  # Schneidet "#?" ab
        
        # 3) In URLSearchParams umwandeln
        search_params = URLSearchParams(param_str)
        
        # Prüfen, ob "AccountNo" als Parameter vorhanden ist
        if not search_params.has("AccountNo"):
            self.textbalances.text = "Es wurde kein Parameter 'AccountNo' gefunden."
            return
        
        # 4) Den Wert von "AccountNo" auslesen
        value = search_params.get("AccountNo")
        
        # Prüfen, ob der Wert überhaupt gefüllt ist
        if not value:
            self.textbalances.text = "Der Parameter 'AccountNo' ist leer."
            return
        
        # 5) Erst jetzt Server-Funktion aufrufen
        result = anvil.server.call('loginaccountnum', value)
        self.textbalances.text = result
