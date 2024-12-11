from ._anvil_designer import Form1Template
from anvil import *
import anvil.server


class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        # Handle URL parameters
        self.handle_url_parameters()

    def handle_url_parameters(self):
        """Parse and validate URL query parameters."""
        # Get the current URL
        url = anvil.js.window.location.href
        
        # Parse query parameters using JavaScript
        params = anvil.js.window.location.search
        query = {}
        if params:
            # Remove the "?" at the start and split into key-value pairs
            pairs = params[1:].split("&")
            for pair in pairs:
                key, value = pair.split("=")
                query[key] = value

        # Check for AccountNo in parameters
        if "AccountNo" in query:
            account_no = query["AccountNo"]
            # Validate the input
            if "UNION" in account_no.upper() or ";" in account_no:
                self.textbalances.text = "Unsichere Eingabe erkannt und blockiert!"
            else:
                # Fetch and display the account balance securely
                try:
                    account_balance = anvil.server.call('get_account_balance_by_accountno', account_no)
                    self.textbalances.text = f"Account {account_no}: {account_balance} Euro"
                except Exception as e:
                    self.textbalances.text = f"Fehler bei der Abfrage: {str(e)}"
        else:
            self.textbalances.text="fehler"
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
      all_balances = anvil.server.call('get_all_balances')
      self.textbalances.text = "\n".join([f"Account {acc}: {bal} Euro" for acc, bal in all_balances])
    def text_box_2_pressed_enter(self, **event_args):
      """Handle Enter key in password box"""
      self.button_login_click()
    
