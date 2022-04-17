from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Month= int(request.form['Month'])
        PeriodOfDay= int(request.form['Period_of_day'])
        load_forecasted=float(request.form['load_forecasted'])
        Price_forecasted=float(request.form['Price_forecasted'])
        Temperature=float(request.form['Temperature'])
        CO2Intensity=float(request.form['CO2Intensity'])
        HolidayFlag=request.form['HolidayFlag']
        Energy_produced=float(request.form['Energy_produced'])
        Load_produced=float(request.form['Load_produced'])
        prediction=model.predict([[HolidayFlag,Month,PeriodOfDay,load_forecasted,Price_forecasted,Temperature,CO2Intensity,Energy_produced,Load_produced]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell at any price.")
        else:
            return render_template('index.html',prediction_text="You Can Sell Electricty at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

