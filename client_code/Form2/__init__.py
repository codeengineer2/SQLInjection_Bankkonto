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
    result = anvil.server.call('check_account', account_no_input, pwd_input)
    self.textbalances.text = str(result)

    
