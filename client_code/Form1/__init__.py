from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def button_login_click(self, **event_args):
    """Handle login button click"""
    username = self.text_box_1.text
    password = self.text_box_2.text

    # Check which login mode is selected
    if self.button_unsafe.selected:
        result = anvil.server.call('login_insecure', username, password)
    elif self.button_safe.selected:
        result = anvil.server.call('login_secure', username, password)
    else:
        result = "Bitte wähle einen Typ aus"

    # Display the result in resulttext
    self.resulttext.text = result

  def text_box_2_pressed_enter(self, **event_args):
    """Handle Enter key in password box"""
    self.button_login_click()
