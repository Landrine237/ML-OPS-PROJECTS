from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import joblib


app = Flask(__name__)
model = joblib.load("model.pkl")
@app.route('/predict' , methods = ['POST'])

def predict():
    data = request.get_json()
    input_data = pd.DataFrame([data])
    input_data['gender'] = input_data['gender'].map({'Male':0, 'Female':1})
    input_data = pd.get_dummies(input_data, columns=['country'], drop_first=True)
    expected_columns = [
        'credit_score', 'age', 'gender', 'tenure', 'balance',
        'products_number', 'credit_card', 'active_member', 'estimated_salary',
        'country_Germany', 'country_Spain'
    ]

    for col in expected_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    input_data = input_data[expected_columns]
    prediction = int(model.predict(input_data)[0])
    return jsonify({'churn': prediction})


if __name__ == '__main__' :
    print('flask is starting..')
    app.run(host = '0.0.0.0' , port = 5000 , debug=True)



# def predict() :
#     data = request.get_json()
#     features = np.array(data['features']).reshape(1,-1)
#     prediction = int(model.predict(features)[0])
#     return jsonify({'churn' : prediction})
    #   prediction = int(model.predict(input_data)[0])
    #   return jsonify({'churn': prediction})
