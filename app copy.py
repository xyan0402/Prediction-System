import os
import sys
import logging
from flask import Flask, request, jsonify, render_template, redirect, flash
from flask_cors import CORS
from datetime import datetime
from model import ml_predict
from flask_wtf import Form
from wtforms.fields import IntegerField, SubmitField
from wtforms import validators, ValidationError
import csv
import numpy as np
from flask import send_file
import pandas as pd
import json

class MyForm(Form):
    zipcode = IntegerField('zipcode', [validators.DataRequired(), 
                                       validators.NumberRange(
                                           min = 10000, 
                                           max = 99999
                                       )])
    numBed = IntegerField('numBed')
    numBath = IntegerField('numBath')
    submit = SubmitField('Search my next home!')

# define the app
app = Flask(__name__)
CORS(app) # needed for cross-domain requests, allow everything by default
app.config.update(dict(
    SECRET_KEY="secretkey",
    WTF_CSRF_SECRET_KEY="csrfkey"
))

# logging for heroku
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if request.method == 'POST' and form.validate():
        data = request.form
        zipcode = int(form.data['zipcode'])
        numBed = int(form.data['numBed'])
        numBath = int(form.data['numBath'])
        with open('data/CityLatLong.csv', 'r') as csvfile:
            csvReader = csv.reader(csvfile)
            flag = 0
            for row in csvReader:
                if(row[4]==str(zipcode)):
                    latitude = float(row[0])
                    longitude = float(row[1])
                    city = row[2]
                    state = row[3]
                    flag = 1
                    break

        inputrows = []
        with open('data/properties_0421.csv', 'r') as csvfile:
            csvReader = csv.reader(csvfile)
            i = 0
            for row in csvReader:
                i = i + 1
                if row[8] == str(numBed) and row[9] == str(numBath):
                    inputrows.append([i, float(row[6]), float(row[1]), float(row[2])])

        if flag == 0:
            ml_results = json.dumps("Invalid zipcode or zipcode not support yet! Please come again later!")
            return render_template('index_tmp.html', form = form, ml_results = ml_results)
        else:
            results = ml_predict.ml_predict(zipcode, latitude, longitude, city, state, numBed, numBath)
            results = results[1:-1]
            ml_results, distance = results.split(",")
            ml_results = float(ml_results)
            distance = float(distance)
            ml_results = '{0:.2f}'.format(ml_results)
            distance = '{0:.2f}'.format(distance)
            ml_results_out = "Price prediction: " + ml_results
            distance_out = "Distance to nearest mall: " + distance + " km"
            return render_template('index.html', form = form, ml_results = ml_results_out, distance = distance_out, info = inputrows, fcn1 = "visualData(pRange)")
    return render_template('index.html', form = form)



# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='0.0.0.0',
            port=8080,
            debug=True
            )
