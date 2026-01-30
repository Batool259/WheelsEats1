import sqlite3

db_path = "instance/wheeleats.sqlite"

con = sqlite3.connect(db_path)
cur = con.cursor()

# Alle Spalten der Tabelle restaurant holen
cur.execute("PRAGMA table_info(restaurant);")
cols = [row[1] for row in cur.fetchall()]

if "website" not in cols:
    cur.execute("ALTER TABLE restaurant ADD COLUMN website VARCHAR(255);")
    con.commit()
    print("OK: Spalte 'website' wurde hinzugefügt.")
else:
    print("Info: Spalte 'website' existiert bereits.")

con.close()
