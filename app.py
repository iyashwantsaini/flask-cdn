# importing libraries
import tensorflow
from flask_ngrok import run_with_ngrok
from profanity_check import predict
import numpy as np
from flask_cors import CORS, cross_origin
import tflearn
from flask import Flask, render_template, request, send_file, jsonify
import joblib
import pandas as pd
import json
import os
import pickle
import random
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
nltk.download('punkt')
np.random.seed(1337)

app = Flask(__name__)

# setting up for google colab
run_with_ngrok(app)

# handling Cross Origin Access
CORS(app)

# For hindi profanity check
absurd_list = ['mc', 'bc', 'madarchod', 'bhenchod', 'sex', 'chutiya', 'gaandu']

# storing in local DB (SQLAlchemy)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

inputmail = None


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)
    parent1 = db.relationship('parents_msg', backref='owner')


class parents_msg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)
    owner_id = db.Column(db.Integer, db.ForeignKey('mail.id'))


class students_msg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)

# tokenizing words


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)


@app.route('/signin')
def signin():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'thapar' and password == 'thapar':
        sqlconnection = sqlite3.connect('db.sqlite3')
        df = pd.read_sql_query("SELECT * FROM mail", sqlconnection)
        return render_template('database.html', tables=[df.to_html(render_links=True, classes=['table table-striped table-bordered table-hover table-responsive text-white'])])
    else:
        return render_template('login.html', warning='Please enter correct username and password!')


@app.route('/email', methods=['GET', 'POST'])
@cross_origin()
def email():
    content = request.json
    msg = content['text']
    msg = msg.lower()
    global inputmail
    inputmail = Mail(mail=msg)
    db.session.add(inputmail)
    db.session.commit()
    new = msg
    return jsonify({'data': new})


@app.route('/email_database', methods=['GET', 'POST'])
def email_database():
    sqlconnection = sqlite3.connect('db.sqlite3')
    df1 = pd.read_sql_query("SELECT * FROM mail", sqlconnection)
    return render_template('database.html', tables=[df1.to_html(render_links=True, classes=['table table-striped table-bordered table-hover table-responsive text-white'])])


@app.route('/chat_database', methods=['GET', 'POST'])
def chat_database():
    sqlconnection = sqlite3.connect('db.sqlite3')
    df = pd.read_sql_query("SELECT * FROM parents_msg", sqlconnection)
    return render_template('database.html', tables=[df.to_html(render_links=True, classes=['table table-striped table-bordered table-hover table-responsive text-white'])])


@app.route('/chat', methods=["POST"])
@cross_origin()
def chat():
    with open("./training_data/detail.json") as file:
        data = json.load(file)
    content = request.json
    msg = content['text']
    msg = msg.lower()
    check = predict([msg])
    if check == 1 or msg in absurd_list:
        send = 'Warning ⚠️ <br> Our Systems detected that you are using absurd language. Please avoid using it. Our system keeps a track of your unique credentials.'
        return jsonify({'data': send})
    else:
        if msg in ['placement', 'campus', 'hostel', 'reach', 'TEQIP', 'library', 'contact', 'scholarships', 'admission']:
            inp = parents_msg(message=msg, owner=inputmail)
            db.session.add(inp)
            db.session.commit()
            new = data[msg]
            return jsonify({'data': new})
        elif msg in ['webkiosk', 'timetable', 'notification', 'extra', 'accreditations', 'examination updates']:
            inp = students_msg(message=msg)
            db.session.add(inp)
            db.session.commit()
            new = data[msg]
            return jsonify({'data': new})
        else:
            inp = parents_msg(message=msg, owner=inputmail)
            db.session.add(inp)
            db.session.commit()
            with open("./training_data/intents.json") as file:
                data = json.load(file)
            try:
                with open("data.pickle", "rb") as f:
                    words, labels, training, output = pickle.load(f)
            except:
                words = []  # list of all word in pattern
                labels = []  # tags with the pattern
                docs_x = []  # words in pattern
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
            net = tflearn.fully_connected(net, 32)
            net = tflearn.fully_connected(net, 16)
            net = tflearn.fully_connected(
                net, len(output[0]), activation="softmax")
            net = tflearn.regression(net)

            model = tflearn.DNN(net)

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
    db.create_all()
    app.run()
    # app.run(host='0.0.0.0', debug=True, port=4040)
