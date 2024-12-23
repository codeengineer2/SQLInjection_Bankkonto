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
        url=anvil.js.window.location.href
        full_hash_str = anvil.js.window.location.hash
        param_str = full_hash_str[2:]
        search_params = URLSearchParams(param_str)
        value = search_params.get("AccountNo")
        self.textbalances.text = anvil.server.call('loginaccountnum', url, full_hash_str, param_str, value)
