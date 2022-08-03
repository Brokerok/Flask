import json
import random
import string
import csv
import os
import requests
from db import execute_query
from faker import Faker
from utils import render_list


from flask import Flask, request, make_response, jsonify, redirect

app = Flask(__name__)


@app.route("/")
def main():
    return jsonify({"status": "OK"})


@app.route("/bitcoin_rate")
def get_bitcoin_rate():
    currency = request.args.get('currency', 'USD')
    content = requests.get('https://bitpay.com/api/rates')
    list_btc = content.json()
    result = 'Currency not found'
    for i in range(len(list_btc)):
        btc = list_btc[i]
        if btc['code'] == currency:
            result = btc['rate']
    return str(result)


@app.route('/random_users')
def gen_random_users():
    count = request.args.get('count', '100')
    try:
        count = int(count)
    except ValueError:
        return "Error. Count is not integer", 400
    fake = Faker()
    res = []
    for i in range(count):
        res.append(f'{i+1}. {fake.name()} + {fake.email()}')
    return render_list(res)


@app.route("/unique_names")
def get_unique_names():
    result = execute_query("""SELECT FirstName 
                                FROM Customers""")
    return str(len(set(result)))


@app.route("/tracks_count")
def get_tracks_count():
    result = execute_query("""SELECT * 
                                FROM tracks""")
    return str(len(result))


@app.route("/customers")
def get_customers():
    city = request.args.get('city')
    country = request.args.get('country')
    result = execute_query("""SELECT * 
                                FROM Customers""")
    result1 = execute_query("""SELECT * 
                                    FROM Customers
                                    WHERE Country = ?""", (country, ))
    result2 = execute_query("""SELECT * 
                                    FROM Customers
                                    WHERE City = ?""", (city, ))
    result3 = execute_query(f"""SELECT * 
                                    FROM Customers
                                    WHERE Country = '{country}' AND City = '{city}'""")
    if city and country is not None:
        res = result3
    elif city is not None:
        res = result2
    elif country is not None:
        res = result1
    else:
        res = result
    return render_list(res)


def get_requirements():
    f = open('requirements.txt', 'r')
    result = f.read()
    f.close()
    return result


@app.route("/redirect-to-headers")
def get_headers_redirect():
    return redirect('/headers')


@app.route('/headers')
def get_headers():
    response = make_response(
        json.dumps(dict(request.headers), indent=2)
    )
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.route('/mean_data')
def get_mean_data():
    filename = os.path.join(
        os.path.dirname(__file__),
        'requirements.txt'
    )
    with open(filename, 'r') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        weight = 0
        height = 0
        line = 0
        for row in file_reader:
            try:
                weight += float(row[1])
                height += float(row[2])
                line += 1
            except ValueError:
                continue
        w = weight / line
        h = height / line
        return f'Срендний вес:{w}, Средний рост:{h}'


@app.route('/random')
def get_random():
    length = request.args.get('length', '10')
    digits = request.args.get('digits', '0')

    try:
        length = int(length)
    except ValueError:
        return "Error. Length is not integer", 400

    if digits == '1':
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    elif digits == '0':
        chars = string.ascii_lowercase + string.ascii_uppercase
    else:
        return "Error. Digits there can only be 1 or absent", 400

    result = []
    for i in range(length):
        result.append(random.choice(chars))

    return "".join(result)


app.run(debug=True)
