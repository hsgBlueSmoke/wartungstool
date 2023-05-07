import streamlit as st
import sqlite3
import os
import uuid
from datetime import datetime, timezone, timedelta
from streamlit_option_menu import option_menu
import pandas as pd

# 1. as sidebar menu
#with st.sidebar:
#    selected = option_menu("Main Menu", ["Home", 'Settings'], 
#        icons=['house', 'gear'], menu_icon="cast", default_index=1)
#    selected   

# Datenbankverbindung herstellen
conn = sqlite3.connect('datenbank_0.7.db')
c = conn.cursor()

# Ordner für die Bildspeicherung erstellen, wenn er nicht bereits vorhanden ist
if not os.path.exists("bilder"):
    os.mkdir("bilder")

# Funktion zum Speichern des Bildes
def save_image(image):
    # Eindeutigen Dateinamen generieren
    now = datetime.now(timezone.utc) + timedelta(hours=1)
    now_str = now.strftime('%Y%m%d_%H%M%S')
    filename = f"{now_str}_{str(uuid.uuid4())[:8]}.jpg"
    filepath = os.path.join("bilder", filename)

    # Bild speichern
    with open(filepath, "wb") as f:
        f.write(image.getbuffer())

    return filename

# Exportfunktion für die Tabelle "jobs"
def export_jobs_as_csv():
    # Daten aus der Tabelle "jobs" abrufen
    c.execute("SELECT * FROM jobs")
    rows = c.fetchall()

    # Spaltennamen aus dem Cursor extrahieren
    columns = [description[0] for description in c.description]

    # Pandas DataFrame erstellen
    df = pd.DataFrame(rows, columns=columns)

    # CSV-Datei speichern
    df.to_csv('jobs_export.csv', index=False)

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
    #image_id = c.execute("SELECT MAX(image_id) FROM images").fetchone()[0]
    
    if image:
        # Bild speichern und Dateiname in der Datenbank speichern
        filename = save_image(image)
        #c.execute("INSERT INTO images (image_name) VALUES (?)", (filename,))
        #conn.commit()
        #st.success("Bild erfolgreich hochgeladen und gespeichert.")

    # Job-Daten in der Datenbank speichern
    if cleaning_required:
        if cleaning_completed:
            c.execute('INSERT INTO jobs (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, cleaning_type, cleaning_completed, cleaning_employee, image_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, cleaning_type, cleaning_completed, cleaning_employee, filename))
        else:
            c.execute('INSERT INTO jobs (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, cleaning_type, image_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, cleaning_type, filename))
    else:
        c.execute('INSERT INTO jobs (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, image_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (date_time, room, machine, description, reason, duration, completed, employee, cleaning_required, filename))
    conn.commit()
    st.success('Die Daten wurden erfolgreich gespeichert.')
    
if st.button('Speichern und CSV herunterladen'):
    # ...

    # Exportfunktion aufrufen
    export_jobs_as_csv()

    st.success('Die Daten wurden erfolgreich gespeichert und als CSV exportiert.')

    # Datei als Download anbieten
    with open('jobs_export.csv', 'rb') as file:
        st.download_button(label='CSV herunterladen', data=file, file_name='jobs_export.csv', mime='text/csv')

# Datenbankverbindung schließen
conn.close()

# Eingabefelder leeren
date_time = ""
room = ""
machine = ""
description = ""
reason = ""
duration = ""
completed = ""
employee = ""
cleaning_required = ""
cleaning_type = ""
cleaning_completed = ""
cleaning_employee = ""
image = ""
st.empty()
