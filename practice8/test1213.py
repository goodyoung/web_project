from flask import Flask, render_template, redirect, url_for, jsonify

import sqlite3
import pandas as pd
from flask import request, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import database as dt




app = Flask(__name__)
@app.route('/',methods = ['GET','POST'])
def main():
    if request.method == 'POST':
        y = request.form.to_dict()
        print(y['var1'].split(','))
        return render_template('testttt.html')
    
    else: 
        return render_template('testttt.html')


 

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
