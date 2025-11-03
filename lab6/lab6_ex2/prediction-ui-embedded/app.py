# importing Flask and other modules
import json
import logging
import os
from io import StringIO

import pandas as pd
from flask import Flask, request, render_template, jsonify

from diabetes_predictor import DiabetesPredictor

# Flask constructor
app = Flask(__name__)

dp = DiabetesPredictor(os.getenv('MODEL_NAME', 'model.keras'))


# A decorator used to tell the application
# which URL is associated function
@app.route('/checkdiabetes', methods=["GET", "POST"])
def check_diabetes():
    if request.method == "GET":
        return render_template("input_form_page.html")

    elif request.method == "POST":
        prediction_input = [
            {
                "ntp": int(request.form.get("ntp")),  # getting input with name = ntp in HTML form
                "pgc": int(request.form.get("pgc")),  # getting input with name = pgc in HTML form
                "dbp": int(request.form.get("dbp")),
                "tsft": int(request.form.get("tsft")),
                "si": int(request.form.get("si")),
                "bmi": float(request.form.get("bmi")),
                "dpf": float(request.form.get("dpf")),
                "age": int(request.form.get("age"))
            }
        ]
        app.logger.debug("Prediction Input : %s", prediction_input)
        df = pd.read_json(StringIO(json.dumps(prediction_input)), orient='records')
        status = dp.predict_single_record(df)
        app.logger.debug("Prediction Output : %s", status)
        return render_template("response_page.html",
                               prediction_variable=status[0])

    else:
        return jsonify(message="Method Not Allowed"), 405  # The 405 Method Not Allowed should be used to indicate
    # that our app that does not allow the users to perform any other HTTP method (e.g., PUT and  DELETE) for
    # '/checkdiabetes' path