import streamlit as st
import sqlite3
import os
import uuid
from datetime import datetime

# Datenbankverbindung herstellen
conn = sqlite3.connect('datenbank_0.5.db')
c = conn.cursor()

# Ordner für die Bildspeicherung erstellen, wenn er nicht bereits vorhanden ist
if not os.path.exists("bilder"):
    os.mkdir("bilder")

# Funktion zum Speichern des Bildes
def save_image(image):
    # Eindeutigen Dateinamen generieren
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{now}_{str(uuid.uuid4())[:8]}.jpg"
    filepath = os.path.join("bilder", filename)

    # Bild speichern
    with open(filepath, "wb") as f:
        f.write(image.getbuffer())

    return filename

# Streamlit UI-Elemente definieren
date_time = st.date_input('Datum')
room = st.selectbox('Raumnummer', [row[0] for row in c.execute('SELECT room_number FROM rooms')])
machine = st.selectbox('Maschine', [row[0] for row in c.execute('SELECT machine_name FROM machines')])
description = st.text_area('Beschreibung der ausgeführten Arbeiten')
reason = st.selectbox('Grund', [row[0] for row in c.execute('SELECT reason FROM reasons')])
duration = st.slider('Dauer', 1, 24, 1)
completed = st.checkbox('Arbeiten Fertig')
employee = st.selectbox('Mitarbeiter', [row[0] for row in c.execute('SELECT employee_name FROM employees')])
cleaning_required = st.checkbox('Reinigung nötig?')
if cleaning_required:
    cleaning_type = st.selectbox('Reinigung', ['intern', 'extern'])
    cleaning_completed = st.checkbox('Reinigung erledigt')
    cleaning_employee = st.selectbox('Produktionsmitarbeiter', [row[0] for row in c.execute('SELECT employee_name FROM employees')])

image = st.file_uploader("Foto hochladen", type=["jpg", "jpeg", "png"])

# Job speichern
if st.button('Speichern'):
    # ID des zuletzt hochgeladenen Bildes abrufen
    image_id = c.execute("SELECT MAX(image_id) FROM images").fetchone()[0]
    
    if image:
        # Bild speichern und Dateiname in der Datenbank speichern
        filename = save_image(image)
        c.execute("INSERT INTO images (image_name) VALUES (?)", (filename,))
        conn.commit()
        st.success("Bild erfolgreich hochgeladen und gespeichert.")

    # Job-Daten in der Datenbank speichern
    if cleaning_required:
        if cleaning_completed:
            c.execute('INSERT INTO jobs (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, cleaning_type, cleaning_completed, cleaning_employee, image_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, cleaning_type, cleaning_completed, cleaning_employee, image_id))
        else:
            c.execute('INSERT INTO jobs (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, cleaning_type, image_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, cleaning_type, image_id))
    else:
        c.execute('INSERT INTO jobs (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, image_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, image_id))
    conn.commit()
    st.success('Die Daten wurden erfolgreich gespeichert.')

# Datenbankverbindung schließen
conn.close()
