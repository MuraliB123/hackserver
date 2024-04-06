
from flask import Flask, json, render_template, request, session
from flask import jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL, create_engine
from sqlalchemy import text as sql_text
import pandas as pd
from flask_cors import CORS
import numpy as np
app = Flask(__name__, static_folder='static')
CORS(app)
app.secret_key = 'mykey'
@app.route('/')
def  index():
    




    return render_template('index.html')
@app.route('/details',methods=['get','post'])
def  user_health_state():
    if request.method == 'POST':
        name = request.form['name']
        illness = request.form['illness']
        symptoms = request.form['symptoms']
        duration = request.form['duration']
        first_occurrence = request.form['first_occurrence']
        admission_date = request.form['admission_date']
        discharge_date = request.form['discharge_date']
        hospital = request.form['hospital']
        previous_condition = request.form['previous_condition']
        hyper_tension = request.form['hypertension']
        diabetes = request.form['diabetes']
        asthma = request.form['asthma']
        ihd = request.form['ihd']
        smoking = request.form['smoking']
        alcohol = request.form['alcohol']
        tobacco = request.form['tobacco']
        drugs = request.form['drugs']
        selected_procedures = request.form.getlist('procedure')
        data = {
             'name': name,
             'illness': illness,
             'symptoms': symptoms,
             'duration': duration,
             'first_occurrence': first_occurrence,
             'admission_date': admission_date,
             'discharge_date': discharge_date,
             'hospital': hospital,
             'previous_condition': previous_condition,
             'hyper_tension': hyper_tension,
             'diabetes': diabetes,
             'asthma': asthma,
             'ihd': ihd,
             'smoking': smoking,
             'alcohol': alcohol,
             'tobacco': tobacco,
             'drugs': drugs,
            'selected_procedures': selected_procedures
            }
        user_claim_state = json.dumps(data)
        '''print(data['name'])
        print(data['illness'])
        print(data['symptoms'])
        print(data['duration'])
        print(data['first_occurrence'])
        print(data['admission_date'])
        print(data['discharge_date'])
        print(data['hospital'])
        print(data['previous_condition'])
        print(data['hyper_tension'])
        print(data['diabetes'])
        print(data['asthma'])
        print(data['ihd'])
        print(data['smoking'])
        print(data['alcohol'])
        print(data['tobacco'])
        print(data['drugs'])
        print(data['selected_procedures'])'''
        question1 = "whether the symptoms { data[symptoms] } are relevant to the illness { data[illness] } ?"
        prompt = "Consider the symptoms '{data[symptoms]}' and the illness '{data[illness]}'. Based on this information, is it likely that the symptoms are relevant to the illness? Final Output : Just print yes or no without any extra text"
        return prompt

    else:
        return render_template('index.html')

# patient health status is relevant to illness and symptoms claimed.
# treatment given and the diagnosis are relevant to each other.
# diagnotics results leads to the preferred tests filed currently.

# analyse the diagnotics results over past few months leads to current proposed tests.



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)