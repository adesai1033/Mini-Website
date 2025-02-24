from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import random

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

#Sets index.html as landing page
@app.route('/')
def index():
    return render_template('index.html')

#called from index.html when there is change in dropdown menu state to "Add Patient"
@app.route('/add')
def add():
    return render_template('add.html')

#called from index.html when there is change in dropdown menu state to "Delete Patient"
@app.route('/delete')
def delete():
    all_patients = get_patients() #want to display db contents when page is loaded
    return render_template('delete.html', all_patients=all_patients)

#selects all patients from db
def get_patients():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM patients;')
    return cursor.fetchall()

#called from add.html when there is change in dropdown menu state to "Add Patient"
@app.route('/add_patient', methods=['POST'])
def add_patient():

    first_name = request.form['firstName']
    last_name = request.form['lastName']
        
        # Connect to the database
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    # Create the table if it doesn't exist, with pid as the primary key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients(
            pid INTEGER PRIMARY KEY,
            firstname TEXT,
            lastname TEXT
        );
    ''')

    #randomly generate patient id
    patient_id = random.randint(1000, 9999)
    #check that patient_id does not already exist in db
    cursor.execute('SELECT pid FROM patients WHERE pid = ?;', (patient_id,))
    
    while cursor.fetchone() is not None: #if fetchone returns a value, patient_id already exists in db
        patient_id = random.randint(1000, 9999) #generate new patient_id
        cursor.execute('SELECT pid FROM patients WHERE pid = ?;', (patient_id,)) #reselect with newly generated id
        #continue loop until a unique patient_id is found

    #once we have ensured patient_id is unique, insert into db
    cursor.execute('INSERT INTO patients (pid, firstname, lastname) VALUES (?, ?, ?);', (patient_id, first_name, last_name))
    connection.commit() #saves changes to db

    all_patients = get_patients() #get updated list of patients
    connection.close() #insertion complete, close connection

    #rerender add.html with updated list of patients
    return render_template('add.html', all_patients=all_patients)

@app.route('/delete_patient', methods=['POST'])
def delete_patient():

    first_name = request.form['firstName']
    last_name = request.form['lastName']
        
    #connect to db
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    #select patient from db to ensure they exist before trying to delete
    cursor.execute('SELECT pid FROM patients WHERE firstname = ? AND lastname = ?;', (first_name, last_name))
    if cursor.fetchone() is not None: #if patient exists
        #delete all entries with same first and last name
        cursor.execute('DELETE FROM patients WHERE firstname = ? AND lastname = ?;', (first_name, last_name))
        connection.commit()
    #get updated patients using helper get_patients and re render delete.html
    return render_template('delete.html', all_patients=get_patients())
   
        
if __name__ == "__main__":
    app.run()

