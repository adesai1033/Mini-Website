from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import random

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/delete')
def delete():
    all_patients = get_patients()
    return render_template('delete.html', all_patients=all_patients)


@app.route('/name', methods=['POST', 'GET'])
def name():
    error = None
    if request.method == 'POST':
        result = valid_name(request.form['FirstName'], request.form['LastName'])
        if result:
            return render_template('input.html', error=error, result=result)
        else:
            error = 'invalid input name'
    return render_template('input.html', error=error)


def valid_name(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(firstname TEXT, lastname TEXT);')
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()

def get_patients():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM patients;')
    return cursor.fetchall()

@app.route('/add_patient', methods=['POST', 'GET'])
def add_patient():
    if request.method == 'POST':
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

        # Generate a unique patient_id
        patient_id = random.randint(1000, 9999)
        cursor.execute('SELECT pid FROM patients WHERE pid = ?;', (patient_id,))
        while cursor.fetchone() is not None:
            patient_id = random.randint(1000, 9999)
            cursor.execute('SELECT pid FROM patients WHERE pid = ?;', (patient_id,))

        # Insert the new patient into the database
        cursor.execute('INSERT INTO patients (pid, firstname, lastname) VALUES (?, ?, ?);', (patient_id, first_name, last_name))
        connection.commit()

    # Retrieve all patients from the database
    cursor.execute('SELECT * FROM patients;')
    all_patients = cursor.fetchall()
    connection.close()

    # Render the template with the list of patients
    return render_template('add.html', all_patients=all_patients)

@app.route('/delete_patient', methods=['POST', 'GET'])
def delete_patient():
     if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        
        # Connect to the database
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT pid FROM patients WHERE firstname = ? AND lastname = ?;', (first_name, last_name))
        if cursor.fetchone() is not None:
            cursor.execute('DELETE FROM patients WHERE firstname = ? AND lastname = ?;', (first_name, last_name))
            connection.commit()
            return render_template('delete.html', all_patients=get_patients())
        else:
            return render_template('delete.html', all_patients=get_patients())
        
if __name__ == "__main__":
    app.run()


