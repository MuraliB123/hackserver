
from flask import Flask, json, render_template, request, session
from flask import jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL, create_engine
from sqlalchemy import text as sql_text
import pandas as pd
from flask_cors import CORS
import numpy as np
import PyPDF2
import re
app = Flask(__name__, static_folder='static')
CORS(app)
app.secret_key = 'mykey'


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
            text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with a single newline
            text = re.sub(r'\s+', ' ', text)  
        return text
    
def extract_current_conditions(text):
    start_index = text.find("Current Conditions")
    end_index = text.find("Diagnosis")
    if start_index != -1 and end_index != -1:
        return text[start_index:end_index]
    else:
        return "Current conditions section not found."
    
def extract_current_treatments(text):
    start_index = text.find("Treatment Plan")
    end_index = text.find("Recommendations")
    if start_index != -1 and end_index != -1:
        return text[start_index:end_index]
    else:
        return "Current treatments section not found."  
    
@app.route('/',methods=['get','post'])    
def index():
    pdf_path = "/home/murali/Documents/hackserver/Medical Report.pdf"
    text = extract_text_from_pdf(pdf_path)
    current_conditions = extract_current_conditions(text)
    print(current_conditions)
    prompt2 = "Consider the claim issued by the customer as having following symptoms '{data[symptoms]}' and the illness '{data[illness]}' and the preferred tests '{data[selected_procedures]}'. The health status of the customer few months back are as follows '{current_conditions}' based on the information just analyze whether the current claim and the past health status are relevant Final Output : Just print yes or no without any extra text"
    current_treatments = extract_current_treatments(text)
    print(current_treatments)
    prompt3 = "The treatments undertaken by the customer in the past are '{current_treatments}' and the treatments and test required by the customer at present are '{data[selected_procedures]}'. Verfiy whether the past treatments eventually leads to current required treatments plan.verify whether both are corelated or not.just print yes if they are related and no if they are not related. print the boolean value without any extra text"
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
        prompt1 = "Consider the symptoms '{data[symptoms]}' and the illness '{data[illness]}'. Based on this information, is it likely that the symptoms are relevant to the illness? Final Output : Just print yes or no without any extra text"
        return prompt1

    else:
        return render_template('index.html')

#prompt 1 
# "Consider the symptoms '{data[symptoms]}' and the illness '{data[illness]}'. Based on this information, is it likely that the symptoms are relevant to the illness? Final Output : Just print yes or no without any extra text"
#prompt2 
# "Consider the claim issued by the customer as having following symptoms '{data[symptoms]}' and the illness '{data[illness]}' and the preferred tests '{data[selected_procedures]}'. The health status of the customer few months back are as follows '{current_conditions}' based on the information just analyze whether the current claim and the past health status are relevant .Final Output : Just print relevant or not relevant without any extra text"
#prompt3
# "The treatments undertaken by the customer in the past are '{current_treatments}' and the treatments and test required by the customer at present are '{data[selected_procedures]}'. Verfiy whether the past treatments eventually leads to current required treatments plan.Final Output : Just print relevant or not relevant without any extra text"

  


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)