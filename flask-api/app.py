from flask import Flask,url_for,redirect,render_template,request,jsonify
from flask_cors import CORS, cross_origin
import os
import numpy as np
import pandas as pd
import random
import pymysql
import json
def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='1234',
                                db='dump_clinic')


import pickle
import re
import sys

from joblib import dump, load

application = Flask(__name__)
app = application

CORS(app)
app.config.update(
    PROPAGATE_EXCEPTIONS = True
)
@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/<int:number>/')
def square(number):
    return jsonify(number=number,
                   square=number**2)

@app.route('/api/intervencio/<int:year>/')
def intervencio(year):
    connection = obtener_conexion()
    data = []
    query = """SELECT COUNT(*) FROM dump_clinic.RegistreQuirofan
        WHERE YEAR(T_entrada_quirofan_H2)=%s
        """%year
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/api/plot')
def plot():
    connection = obtener_conexion()
    query="""SELECT serveis_id, COUNT(serveis_id) FROM INTERVENCIO WHERE serveis_id IS NOT NULL GROUP BY serveis_id"""

    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    connection.close()
    dataset=pd.DataFrame(data)
    df = dataset
    x = [int(i) for i in list(df[0])]
    y = [int(i) for i in list(df[1])]
    d = [{'x': x, 'y': y} for x, y in zip(df[0], df[1])]
    return jsonify(x = x, y = y)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)