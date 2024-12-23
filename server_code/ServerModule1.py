import anvil.server
import sqlite3
import anvil.files
from anvil.files import data_files
import anvil.http
import anvil.js

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
def get_balance_by_username(username):
    """
    Gibt den Kontostand eines Nutzers anhand seines Benutzernamens zurück.
    Falls kein Nutzer gefunden wird, gibt die Funktion None zurück.
    """
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    query = """
        SELECT Balances.balance
        FROM Users
        JOIN Balances ON Users.AccountNo = Balances.AccountNo
        WHERE Users.username = ?
    """
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    db.close()

    if row:
        return f"Dein Kontostand ist: {row[0]}€"
    else:
        return None


@anvil.server.callable
def loginaccountnum(value):
    """
    Unsicheres Beispiel:
      - Baut den SQL-Abfrage-String durch String-Konkatenation (anfällig für SQL-Injection).
      - Gibt alle (username, balance) für diese AccountNo aus.
      - Falls gefunden, wird formatiert: "Welcome [...]! Your balance is [...]."
    """

    query = f"""
        SELECT Users.username, Balances.balance
        FROM Users
        JOIN Balances ON Users.AccountNo = Balances.AccountNo
        WHERE Balances.AccountNo = {value}
    """
    print("SQL-Query:", query)

    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute(query)        
    all_rows = cursor.fetchall()
    db.close()

    if not all_rows:
        return f"Kein Eintrag mit AccountNo={value} gefunden"
    

    user_list = [row[0] for row in all_rows]
    balance_list = [row[1] for row in all_rows]

    return f"Welcome {user_list}! Your balance is {balance_list}."