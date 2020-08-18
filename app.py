import langdetect
from langdetect import detect
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy
from googletrans import Translator
translator = Translator()


def getdata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
    }
    return requests.get(url, headers=headers).text


app = Flask(__name__)
CORS(app)


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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    # app.run()
