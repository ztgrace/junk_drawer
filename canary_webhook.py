#!/usr/bin/env python
# A simple script to catch canarytokens (https://github.com/thinkst/canarytokens) webhooks

from flask import Flask, request, render_template, flash, url_for, make_response
from os.path import exists
import sqlite3

DB = "canary.db"
app = Flask(__name__, static_url_path='/static')
app.debug = True

@app.route('/', methods=['GET'])
def default():
        return "Ok"

@app.route('/canary', methods=['POST'])
def handle_canary():
        json = request.get_json()
        src_ip = json['additional_data']['src_ip']
        channel = json['channel']
        raw = request.data

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO hits (src_ip, channel, raw) VALUES (?, ?, ?)", (src_ip, channel, raw))
        connection.commit()
        connection.close()

        return "Ok"

if not exists(DB):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE hits (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, src_ip TEXT, channel TEXT, raw TEXT)")
        conn.commit()
        conn.close()

app.run(host='0.0.0.0', port=80)
