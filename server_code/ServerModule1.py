import anvil.server
import sqlite3
import anvil.files
from anvil.files import data_files
import anvil.http
db_path = data_files['database.db']

@anvil.server.callable
def login_insecure(username, password):
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()

            query = f"""
                SELECT Users.username, Balances.balance 
                FROM Users 
                JOIN Balances ON Users.AccountNo = Balances.AccountNo 
                WHERE Users.username = '{username}' AND Users.password = '{password}'

            """
            user = cursor.execute(query).fetchone()
            
            if user:
                return "Eingeloggt!"
            else:
                return "Login fehlgeschlagen!"
    except Exception as e:
        return f"Fehler: {str(e)}"


@anvil.server.callable
def login_secure(username, password):
    """
    Sichere Login-Funktion: Verwendet Parameter Binding.
    Dadurch wird SQL-Injection erschwert.
    """
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            
            query = """
                SELECT Users.username, Balances.balance
                FROM Users
                JOIN Balances ON Users.AccountNo = Balances.AccountNo
                WHERE Users.username = ? AND Users.password = ?
            """
            user = cursor.execute(query, (username, password)).fetchone()
            
            if user:
                return "Eingeloggt!"
            else:
                return "Login fehlgeschlagen!"
    except Exception as e:
        return f"Fehler: {str(e)}"

@anvil.server.callable
def get_balance(account_no):
    """
    Fragt den Kontostand zu einer Account-Nummer ab.
    Gibt 'None' zurück, falls es keinen Eintrag in der DB gibt.
    """
    db = sqlite3.connect("database.db")  # Deine SQLite-DB
    cursor = db.cursor()
    
    # Führe eine SELECT-Abfrage aus
    row = cursor.execute(
        "SELECT balance FROM Balances WHERE AccountNo = ?", 
        (account_no,)
    ).fetchone()

    db.close()

    if row:
        return row[0]  # Der gefundene Kontostand
    else:
        return None