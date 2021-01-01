import tensorflow
import numpy as np
from flask_cors import CORS, cross_origin
import tflearn
from flask import Flask, request, jsonify
import pandas as pd
import json
import os
import pickle
import random
import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
nltk.download('punkt')
np.random.seed(1337)

app = Flask(__name__)
CORS(app)

# tokenize the words and return list
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)


detail_list = ['placement', 'campus life', 'accreditations', 'hostel', 'webkiosk', 'reach', 'TEQIP',
               'timetable', 'examination updates', 'library', 'contact', 'notification', 'extra', 'scholarship', 'admission', 'pulse', 'research', 'lmtsm', 'eligibility', 'academics']


@app.route('/chat', methods=["POST"])
@cross_origin()
def chat():
    # get user input in lowercase
    content = request.json
    msg = content['text']
    msg = msg.lower()

    # try with static data
    with open("detail.json") as file:
        data = json.load(file)
    if msg in detail_list:
        response_ = data[msg]
        return jsonify({'data': response_})

    # else train or use already trained model
    else:
        with open("intents.json") as file:
            data = json.load(file)
        try:
            with open("data.pickle", "rb") as f:
                words, labels, training, output = pickle.load(f)
        except:
            words = []
            labels = []
            docs_x = []
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
        responses = []
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
    return jsonify({'data': random.choice(responses)})


if __name__ == '__main__':
    app.run()
