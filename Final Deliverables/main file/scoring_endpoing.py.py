#importing required libraries

from flask import Flask, request, render_template, Flask, g,redirect,render_template,request,session,url_for
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "<Ju1FjIkffMI4-YpsZ2Q7xwMMc7cvM7s--7T4yKxslbLh>"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        return redirect(url_for('profile'))

    return render_template('login.html')


@app.route("/detect", methods=["GET", "POST"])
def profile():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 
        payload_scoring = {"input_data": [{"fields": [["f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16","f17","f18","f19","f20""f21","f22","f23","f24","f25","f26","f27""f28","f29"]], "values":url}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/cf4dbe2d-e2c4-4487-aa3c-f9c4a7674a58/predictions?version=2022-11-17', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        payload_scoring = {"input_data": [{"fields": [["f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16","f17","f18","f19","f20""f21","f22","f23","f24","f25","f26","f27""f28","f29"]], "values":url}]}
        print("Scoring response")
        print(response_scoring.json())

        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('profile.html',xx =round(y_pro_non_phishing,2),url=url )
    return render_template("profile.html", xx =-1)


if __name__ == "__main__":
    app.run(debug=False)