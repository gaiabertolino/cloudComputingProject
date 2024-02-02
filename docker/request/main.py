import os
from flask import Flask, app, request
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import emailSender
import PySimpleGUI as sg
from http.server import BaseHTTPRequestHandler, HTTPServer


def algo(data, algorithm):
   # Transforming in array
    dataset = []
    for i in range(0, len(data)):
        dataset.append([str(data.values[i,j]) for j in range(0, len(data.iloc[0]))])

    # Onehotencoding of data
    encoder = TransactionEncoder()
    oneHotEncoder = encoder.fit(dataset).transform(dataset)
    enc = pd.DataFrame(oneHotEncoder, columns=encoder.columns_)

    # Extracting the most frequest itemsets via Mlxtend
    if algorithm == "Apriori":
        frequent_itemsets = apriori(enc, min_support=0.01, use_colnames=True)
    else:
        frequent_itemsets = fpgrowth(enc, min_support=0.01, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    
    # Saving the result in a txt
    np.savetxt(r'result.txt', frequent_itemsets.values, fmt='%s', header=' '.join(frequent_itemsets.columns))


def algorithm(path, algorithm, mail):
    # Loading the Data
    file = open(path, "r")
    try:
        data = pd.read_csv(file, sep="\s+|;|:")
        algo(data, algorithm)
        # Sending results
        body = "Attached to this email you will find the file containing the result of the algorithm on your dataset. \nThank you for using our program"
        emailSender.send_email("projectestergab@gmail.com", "imegxudwovmssgzg", mail, "Your result", "result.txt", body)
    except: 
        body = "We found trouble with your csv file. Please take a look and submit it again. \nThank you for using our program"
        emailSender.send_email("projectestergab@gmail.com", "imegxudwovmssgzg", mail, "Your result", "", body)
    
app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        path = str(os.getcwd() + "\\" + request.files['file'].filename)
        request.files['file'].save(path)
        algorithm(path, request.form['algorithm'], request.form['mail'])
    else:
        return "Error password or user not match"
    return "Error password or user not match"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


    