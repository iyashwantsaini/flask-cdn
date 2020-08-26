from flask import Flask, render_template, request, jsonify
import tensorflow
import numpy as np
import os
import pickle
import random
import tflearn
from nltk.stem.lancaster import LancasterStemmer
import nltk
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import langdetect
from langdetect import detect
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy
from googletrans import Translator
translator = Translator()


stemmer = LancasterStemmer()
nltk.download('punkt')
np.random.seed(1337)


def getdata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
    }
    return requests.get(url, headers=headers).text

city_list = ["andhra pradesh", "arunachal pradesh ", "assam", "bihar", "chhattisgarh", "goa", "gujarat", "haryana", "himachal pradesh", "jammu and kashmir", "jharkhand", "karnataka", "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland",
             "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura", "uttar pradesh", "uttarakhand", "west bengal", "andaman and nicobar Islands", "chandigarh", "dadra and nagar haveli", "daman and diu", "lakshadweep", "delhi", "puducherry", "rajasthan", "jharkhand"]

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(50))
    message = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(50))
    mail = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)

# db.create_all()


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/hosp', methods=['GET', 'POST'])
def hosp():
    content = request.json
    msg = content['text']
    language = content['lang']
    print(language)
    if language == 'en':
        msg = msg.lower()
        with open("hospitals.json", encoding='utf-8') as f:
            data = json.load(f)
        send = data[msg]
        return jsonify({'data': send})

    elif language == 'hi':
        print(language)
        with open("hospitals.json", encoding='utf-8') as f:
            data = json.load(f)
        msg = translator.translate(msg, dest='en')
        msg = msg.text
        msg = msg.lower()
        send = data[msg]
        send = translator.translate(send, dest='hi')
        print(send[0].text)
        return jsonify({'data': send[0].text})


@app.route('/lines', methods=['GET', 'POST'])
def lines():
    content = request.json
    msg = content['text']
    language = content['lang']
    if language == 'en':
        msg = msg.lower()
        print('i am ok')
        with open("helpline.json", encoding='utf-8') as f:
            data = json.load(f)
        send = data[msg]
        return jsonify({'data': send})

    elif language == 'hi':
        with open("helpline.json", encoding='utf-8') as f:
            data = json.load(f)
        msg = translator.translate(msg, dest='en')
        msg = msg.text
        msg = msg.lower()
        send = data[msg]
        send = translator.translate(send, dest='hi')
        return jsonify({'data': send[0].text})

    else:
        print('--')


@app.route('/prec', methods=['GET', 'POST'])
def prec():
    content = request.json
    language = content['lang']
    if language == 'en':
        with open("helpline.json", encoding="utf8") as f:
            data = json.load(f)
        send = data['precautions']
        return jsonify({'data': send})

    elif language == 'hi':
        with open("helpline.json", encoding="utf8") as f:
            data = json.load(f)
        send = data['precautions']
        send = translator.translate(send, dest='hi')
        return jsonify({'data': send[0].text})


@app.route('/track', methods=['GET', 'POST'])
def track():
    content = request.json
    language = content['lang']
    state = []
    confirm_cases = []
    cured_cases = []
    death_cases = []
    Active_Cases, Cured, Deaths = 0, 0, 0
    data = getdata(
        "https://www.mygov.in/corona-data/covid19-statewise-status/")

    soup = BeautifulSoup(data, "lxml")

    Active = soup.find('div', {
                       'class': 'field field-name-field-total-active-case field-type-number-integer field-label-above'})
    Active_Cases = Active.text.split()[2]

    Cured = soup.find('div', {
                      'class': 'field field-name-field-total-cured-discharged field-type-number-integer field-label-above'})
    Cured = Cured.text.split()[1]

    Deaths = soup.find('div', {
                       'class': 'field field-name-field-total-death-case field-type-number-integer field-label-above'})
    Deaths = Deaths.text.split()[1]

    names = soup.find_all('div', {
                          'class': 'field field-name-field-select-state field-type-list-text field-label-above'})

    confirmed = soup.find_all('div', {
                              'class': 'field field-name-field-total-confirmed-indians field-type-number-integer field-label-above'})

    cured = soup.find_all('div', {
                          'class': 'field field-name-field-cured field-type-number-integer field-label-above'})

    deaths = soup.find_all('div', {
                           'class': 'field field-name-field-deaths field-type-number-integer field-label-above'})

    for name in names:
        tem = name.text.split()
        state.append(' '.join(tem[2:]))

    for confirm in confirmed:
        confirm_cases.append(confirm.text.split()[2])

    for i in cured:
        cured_cases.append(i.text.split()[3])

    for death in deaths:
        death_cases.append(death.text.split()[1])

    if language == 'en':
        send = str('Total Active Cases In India: '+Active_Cases+'<br>' +
                   'Total cured cases: '+Cured+'<br>'+'Total Deaths in India: '+Deaths)
        return jsonify({'data': send})

    elif language == 'hi':
        send = str('भारत में कुल सक्रिय मामले:  '+Active_Cases+'<br>' +
                   'कुल ठीक मामले: '+Cured+'<br>'+'भारत में कुल मौतें: '+Deaths)

        return jsonify({'data': send})


@app.route('/trackstate', methods=['GET', 'POST'])
def trackstate():
    content = request.json
    msg1 = content['text']
    language = content['lang']
    if language == 'en':
        msg = msg1.lower()
        state = []
        state_lower = []
        confirm_cases = []
        cured_cases = []
        death_cases = []
        Cured, Deaths = 0, 0
        print(msg)
        data = getdata(
            "https://www.mygov.in/corona-data/covid19-statewise-status/")

        soup = BeautifulSoup(data, "lxml")

        Cured = soup.find('div', {
                          'class': 'field field-name-field-total-cured-discharged field-type-number-integer field-label-above'})
        Cured = Cured.text.split()[1]

        Deaths = soup.find('div', {
                           'class': 'field field-name-field-total-death-case field-type-number-integer field-label-above'})
        Deaths = Deaths.text.split()[1]

        names = soup.find_all('div', {
                              'class': 'field field-name-field-select-state field-type-list-text field-label-above'})

        confirmed = soup.find_all('div', {
                                  'class': 'field field-name-field-total-confirmed-indians field-type-number-integer field-label-above'})

        cured = soup.find_all('div', {
                              'class': 'field field-name-field-cured field-type-number-integer field-label-above'})

        deaths = soup.find_all('div', {
                               'class': 'field field-name-field-deaths field-type-number-integer field-label-above'})

        for name in names:
            tem = name.text.split()
            state.append(' '.join(tem[2:]))

        for confirm in confirmed:
            confirm_cases.append(confirm.text.split()[2])

        for i in cured:
            cured_cases.append(i.text.split()[3])

        for death in deaths:
            death_cases.append(death.text.split()[1])

        for name in state:
            new = name.lower()
            state_lower.append(new)

        data = {'States': state_lower, 'Confirm Cases': confirm_cases,
                'Cured Cases': cured_cases, 'Death Cases': death_cases}
        df = pd.DataFrame.from_dict(data)
        df = df.set_index(df.columns[0])
        confirm1 = df.loc[msg, 'Confirm Cases']
        cured1 = df.loc[msg, 'Cured Cases']
        death1 = df.loc[msg, 'Death Cases']

        send = str('State: '+msg.capitalize()+'<br>'+'Confirmed Cases: '+confirm1 +
                   '<br>'+'Patients Cured: '+cured1+'<br>'+'Total Deaths: '+death1)
        return jsonify({'data': send})

    elif language == 'hi':
        msg = translator.translate(msg1, dest='en')
        msg = msg.text
        msg = msg.lower()
        state = []
        state_lower = []
        confirm_cases = []
        cured_cases = []
        death_cases = []
        Cured, Deaths = 0, 0
        data = getdata(
            "https://www.mygov.in/corona-data/covid19-statewise-status/")

        soup = BeautifulSoup(data, "lxml")

        Cured = soup.find('div', {
                          'class': 'field field-name-field-total-cured-discharged field-type-number-integer field-label-above'})
        Cured = Cured.text.split()[1]

        Deaths = soup.find('div', {
                           'class': 'field field-name-field-total-death-case field-type-number-integer field-label-above'})
        Deaths = Deaths.text.split()[1]

        names = soup.find_all('div', {
                              'class': 'field field-name-field-select-state field-type-list-text field-label-above'})

        confirmed = soup.find_all('div', {
                                  'class': 'field field-name-field-total-confirmed-indians field-type-number-integer field-label-above'})

        cured = soup.find_all('div', {
                              'class': 'field field-name-field-cured field-type-number-integer field-label-above'})

        deaths = soup.find_all('div', {
                               'class': 'field field-name-field-deaths field-type-number-integer field-label-above'})

        for name in names:
            tem = name.text.split()
            state.append(' '.join(tem[2:]))

        for confirm in confirmed:
            confirm_cases.append(confirm.text.split()[2])

        for i in cured:
            cured_cases.append(i.text.split()[3])

        for death in deaths:
            death_cases.append(death.text.split()[1])

        for name in state:
            new = name.lower()
            state_lower.append(new)

        data = {'States': state_lower, 'Confirm Cases': confirm_cases,
                'Cured Cases': cured_cases, 'Death Cases': death_cases}
        df = pd.DataFrame.from_dict(data)
        df = df.set_index(df.columns[0])
        confirm1 = df.loc[msg, 'Confirm Cases']
        cured1 = df.loc[msg, 'Cured Cases']
        death1 = df.loc[msg, 'Death Cases']

        send = str('राज्य:'+msg1+'<br>'+'वे केस जिनकी पुष्टि हो चुकी है : '+confirm1 +
                   '<br>'+'मरीजों को ठीक किया गया : '+cured1+'<br>'+'कुल मौतें : '+death1)
        return jsonify({'data': send})


@app.route('/signin')
def signin():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'thapar' and password == 'thapar':
        cnx = sqlite3.connect('db.sqlite3')
        df = pd.read_sql_query("SELECT * FROM mail", cnx)
        # email database in form of dataframe
        #df1 = pd.read_sql_query("SELECT * FROM user", cnx)
        return render_template('table.html', tables=[df.to_html(render_links=True, classes=['table table-striped table-bordered table-hover table-responsive text-white'])])

    elif username == 'chatbot' and password == 'myways':
        cnx = sqlite3.connect('db.sqlite3')
        df = pd.read_sql_query("SELECT * FROM mail", cnx)
        # email database in form of dataframe
        #df1 = pd.read_sql_query("SELECT * FROM user", cnx)
        return render_template('table.html', tables=[df.to_html(render_links=True, classes=['table table-striped table-bordered table-hover table-responsive text-white'])])

    else:
        return render_template('login.html', warning='Please enter correct username and password')


@app.route('/email', methods=['GET', 'POST'])
@cross_origin()
def email():
    content = request.json
    msg = content['text']
    msg = msg.lower()
    print('mail')
    user = Mail(mail=msg)
    db.session.add(user)
    db.session.commit()
    new = msg
    return jsonify({'data': new})


@app.route('/email_database', methods=['GET', 'POST'])
# @login_required
def email_database():
    cnx = sqlite3.connect('db.sqlite3')
    df1 = pd.read_sql_query("SELECT * FROM mail", cnx)
    return render_template('table.html', tables=[df1.to_html(render_links=True, classes=['table table-striped table-bordered table-hover table-responsive text-white'])])


@app.route('/chat_database', methods=['GET', 'POST'])
# @login_required
def chat_database():
    cnx = sqlite3.connect('db.sqlite3')
    df = pd.read_sql_query("SELECT * FROM user", cnx)
    return render_template('table.html', tables=[df.to_html(render_links=True, classes=['table table-striped table-bordered table-hover table-responsive text-white'])])


@app.route('/chat', methods=["POST"])
@cross_origin()
def chat():
    with open("detail.json") as file:
        data = json.load(file)
    content = request.json
    msg = content['text']
    print('ok')
    msg = msg.lower()
    user = User(message=msg)
    db.session.add(user)
    db.session.commit()
    if msg == 'placement':
        print('hello')
        new = data['placement']
        return jsonify({'data': new})
    elif msg == 'campus':
        new = data['campus life']
        return jsonify({'data': new})
    elif msg == 'hostel':
        new = data['hostel']
        return jsonify({'data': new})
    elif msg == 'webkiosk':
        new = data['webkiosk']
        return jsonify({'data': new})
    elif msg == 'reach':
        new = data['reach']
        return jsonify({'data': new})
    elif msg == 'TEQIP':
        new = data['TEQIP']
        return jsonify({'data': new})
    elif msg == 'timetable':
        new = data['timetable']
        return jsonify({'data': new})
    elif msg == 'library':
        new = data['library']
        return jsonify({'data': new})
    elif msg == 'contact':
        new = data['contact']
        return jsonify({'data': new})
    elif msg == 'notification':
        new = data['notification']
        return jsonify({'data': new})
    elif msg == 'extra':
        new = data['extra']
        return jsonify({'data': new})
    elif msg == 'scholarship':
        new = data['scholarships']
        return jsonify({'data': new})
    elif msg == 'admission':
        new = data['admission']
        return jsonify({'data': new})

    else:
        print('hello')
        with open("intents.json") as file:
            data = json.load(file)

        try:
            with open("data.pickle", "rb") as f:
                words, labels, training, output = pickle.load(f)
        except:
            words = []  # list of all word in pattern
            labels = []  # tag with that pattern
            docs_x = []  # patterns ke words
            docs_y = []

            for intent in data["intents"]:
                for pattern in intent["patterns"]:
                    wrds = nltk.word_tokenize(pattern)
                    words.extend(wrds)
                    docs_x.append(wrds)
                    docs_y.append(intent["tag"])

                if intent["tag"] not in labels:
                    labels.append(intent["tag"])

            words = [stemmer.stem(w.lower()) for w in words if w != "?"]
            words = sorted(list(set(words)))

            labels = sorted(labels)

            training = []
            output = []

            out_empty = [0 for _ in range(len(labels))]

            for x, doc in enumerate(docs_x):
                bag = []

                wrds = [stemmer.stem(w.lower()) for w in doc]

                for w in words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)

                output_row = out_empty[:]
                output_row[labels.index(docs_y[x])] = 1

                training.append(bag)
                output.append(output_row)

            training = numpy.array(training)
            output = numpy.array(output)
            with open("data.pickle", "wb") as f:
                pickle.dump((words, labels, training, output), f)

        tensorflow.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 16)
        net = tflearn.fully_connected(net, 16)
        #net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(
            net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)
        # tf.compat.v1.reset_default_graph()
        # define the keras model
        '''model = Sequential() 
        model.add(Dense(8, activation='relu', input_shape=(len(training[0]))))  
        model.add(Dense(8, activation="relu")) 
        model.add(Dense(len(output[0]), activation="softmax"))  
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy']) 
        #history = model.fit(training,output, epochs=100, batch_size=20) '''
        MODEL_NAME = 'model.tflearn'
        if os.path.exists(MODEL_NAME + ".meta"):
            model.load(MODEL_NAME)
        else:
            model.fit(training, output, n_epoch=1200,
                      batch_size=8, show_metric=True)
            model.save(MODEL_NAME)

        results = model.predict([bag_of_words(msg, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

    return jsonify({'data': random.choice(responses)})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    # app.run()
