from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.button_login_click()
    # Any code you write here will run before the form opens.
  

  def button_login_click(self, **event_args):
    
      username = self.text_box_1.text
      password = self.text_box_2.text

      if self.button_unsafe.selected:
        result = anvil.server.call('login_insecure', username, password)
      elif self.button_safe.selected:
        result = anvil.server.call('login_secure', username, password)
      else:
        result = "Bitte wähle einen Typ aus"
        

      self.resulttext.text = result

