import sqlite3
import os
from datetime import datetime

# Verzeichnis, in dem das Skript und die Datenbankdatei gespeichert sind
base_dir = os.path.abspath(os.path.dirname(__file__))

# Pfad zur Datenbankdatei
db_path = os.path.join(base_dir, "datenbank_0.5.db")

# Erstellen der Verbindung zur Datenbank
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Erstellen der Tabellen
c.execute('''CREATE TABLE IF NOT EXISTS rooms (
                room_number INTEGER PRIMARY KEY,
                room_name TEXT
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS machines (
                machine_id INTEGER PRIMARY KEY,
                machine_name TEXT
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS reasons (
                reason_id INTEGER PRIMARY KEY,
                reason TEXT
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY,
                employee_name TEXT
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS images (
                image_id INTEGER PRIMARY KEY,
                job_id INTEGER,
                image_name TEXT,
                FOREIGN KEY(job_id) REFERENCES jobs(job_id)
             )''')


c.execute('''CREATE TABLE IF NOT EXISTS jobs (
                job_id INTEGER PRIMARY KEY,
                date_time TEXT,
                room INTEGER,
                machine INTEGER,
                description TEXT,
                reason INTEGER,
                duration INTEGER,
                completed INTEGER,
                employee INTEGER,
                cleaning_required INTEGER,
                cleaning_type TEXT,
                cleaning_completed INTEGER,
                cleaning_employee INTEGER,
                image_id INTEGER,
                FOREIGN KEY(room) REFERENCES rooms(room_number),
                FOREIGN KEY(machine) REFERENCES machines(machine_id),
                FOREIGN KEY(reason) REFERENCES reasons(reason_id),
                FOREIGN KEY(employee) REFERENCES employees(employee_id),
                FOREIGN KEY(cleaning_employee) REFERENCES employees(employee_id)
             )''')

# Beispiel-Daten einfügen
c.execute("INSERT INTO rooms (room_number, room_name) VALUES (101, 'Raum 101')")
c.execute("INSERT INTO rooms (room_number, room_name) VALUES (102, 'Raum 102')")

c.execute("INSERT INTO machines (machine_id, machine_name) VALUES (1, 'Maschine A')")
c.execute("INSERT INTO machines (machine_id, machine_name) VALUES (2, 'Maschine B')")

c.execute("INSERT INTO reasons (reason_id, reason) VALUES (1, 'Wartung')")
c.execute("INSERT INTO reasons (reason_id, reason) VALUES (2, 'Reparatur')")

c.execute("INSERT INTO employees (employee_id, employee_name) VALUES (1, 'Max Mustermann')")
c.execute("INSERT INTO employees (employee_id, employee_name) VALUES (2, 'Anna Schmidt')")


# Ein Beispiel-Job einfügen
now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")
room = 101
machine = 1
description = "Beispieljob"
reason = 1
duration = 2
completed = 1
employee = 1
cleaning_required = 0

c.execute("INSERT INTO jobs (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
          (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required))

# Datenbank-Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("Datenbank wurde erstellt und Beispiel-Daten wurden hinzugefügt.")
