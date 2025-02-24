# Flask Web Application

## Overview
This is a web-based application built using Flask, The application provides a simple interface adding and deleting patient names to/from the hospital database. The application has a landing page with a dropdown menu to select the action to be performed (add or delete). Selection of add or delete will redirect to the respective html pages. Each page has a form where you must inputed the patient's first and last name. Both fields are required. We have also included a back button on both pages to redirect to the landing page.
## Features
- **Add Data**: Users can add new entries through a form interface
- **View Data**: Display all stored data in a tabular format
- **Delete Data**: Remove existing entries from the database

## Requirements
Make sure to have python installed on your system. pip install flask. 

## Usage
python -m venv venv <br />
source .venv/bin/activate <br />
pip install -r requirements.txt <br />
python app.py


