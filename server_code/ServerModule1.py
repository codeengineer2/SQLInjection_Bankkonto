import anvil.server
import sqlite3
import anvil.files
from anvil.files import data_files

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
def get_all_balances():
    """
    Gibt alle (AccountNo, balance) zurück.
    """
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            query = "SELECT AccountNo, balance FROM Balances"
            balances = cursor.execute(query).fetchall()
            return balances  # Liste von Tupeln [(1, 100.0), (2, 50.0), ...]
    except Exception as e:
        return f"Fehler: {str(e)}"


@anvil.server.callable
def get_account_balance_by_accountno(account_no):
    """
    Fragt nur den Kontostand eines bestimmten Accounts ab.
    (In diesem Beispiel für Level2 nicht zwingend benötigt,
     da wir alle Balances auf einmal holen.)
    """
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            query = "SELECT balance FROM Balances WHERE AccountNo = ?"
            balance = cursor.execute(query, (account_no,)).fetchone()
            if balance:
                return balance[0]
            else:
                return "Kein Kontostand gefunden"
    except Exception as e:
        return f"Fehler: {str(e)}"

@anvil.server.callable
def get_all_balances_insecure(account_no):
    """
    Unsichere Abfrage, die den Parameter `account_no` direkt ins SQL-Statement
    einsetzt und somit SQL-Injection erlaubt.
    """
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()

            # Achtung: Unsicheres Statement!
            # Hier wird account_no (z.B. "0 OR 1=1") unverändert eingebaut.
            query = f"""
                SELECT Users.username, Balances.balance
                FROM Users
                JOIN Balances ON Users.AccountNo = Balances.AccountNo
                WHERE Users.AccountNo = {account_no}
            """
            # Wenn account_no = "0 OR 1=1", lautet die WHERE-Klausel:
            #  WHERE Users.AccountNo = 0 OR 1=1
            # => TRUE => Alle Zeilen werden zurückgegeben.

            rows = cursor.execute(query).fetchall()

            # rows könnte z.B. [(admin1, 5000), (frodo, 1500), (glorfindel, 7500)]
            if rows:
                usernames = [r[0] for r in rows]  # Liste aller Usernames
                balances = [r[1] for r in rows]   # Liste aller Balances
                return f"Willkommen {usernames}! Balances: {balances}"
            else:
                return "Keine Daten gefunden."
    except Exception as e:
        return f"Fehler: {str(e)}"