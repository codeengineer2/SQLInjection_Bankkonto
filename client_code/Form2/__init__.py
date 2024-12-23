from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.js

import anvil.server
import anvil.http

class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def button_check_click(self, **event_args):
    # Nutzereingaben aus den Textboxen abholen
    account_no_input = self.text_box_account_no.text
    pwd_input = self.text_box_pwd.text

    # Server-Funktion aufrufen, die (unsicher) in die DB schaut
    result = anvil.server.call('check_account', account_no_input, pwd_input)

    # Ergebnis im Label anzeigen
    self.textbalances.text = str(result)
  