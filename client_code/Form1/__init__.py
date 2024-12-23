from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)

    def perform_login(self, mode):
        """
        'mode' kann z.B. 'unsafe' oder 'safe' sein.
        Der eigentliche Login-Code steckt hier drin.
        """
        username = self.text_box_1.text
        password = self.text_box_2.text

        if mode == "unsafe":
            result = anvil.server.call('login_insecure', username, password)
            self.textbalances.text = "Das ist unsafe"
        else:  # mode == "safe"
            result = anvil.server.call('login_secure', username, password)
        
        if result == "Eingeloggt!":
            self.label_status.text = result
          
            open_form('Form2')
        else:
            self.label_status.text = result

    def button_unsafe_click(self, **event_args):
        pass

    def button_safe_click(self, **event_args):
        pass

    def text_box_2_pressed_enter(self, **event_args):
        """
        Wird aufgerufen, sobald man im Passwort-Feld Enter drückt.
        Hier kannst du ebenfalls entscheiden, ob du 'unsafe' oder 'safe' wählst.
        """
        # Beispiel: standardmäßig den sicheren Login nutzen
        #self.perform_login(mode="safe")
    pass

    def button_unsafe_select(self, **event_args):
      """This method is called when the radio button is selected."""
      self.perform_login(mode="unsafe")

    def button_safe_select(self, **event_args):
      """This method is called when the radio button is selected."""
      self.perform_login(mode="safe")
