from flask import Flask, render_template, redirect, url_for
import sqlite3
import pandas as pd
import database as dt   # database 모듈화
from flask import request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        result = request.form.to_dict()
        if result['select1'] =='pos':
            dt.database(1,0)
        else:
            dt.database(0,1)
        user_name=result['name']
        dt.commit_name(user_name)
        return redirect(url_for('result'))
    
    else:
        return render_template('index.html')
#checkbox에서 
# name : 전달할 값의 이름이다.
# value : 전달될 값이다.

@app.route("/result",methods=['GET','POST'])
def result():
    result_pos,result_neg = dt.database()
    name = dt.commit_name()
    return render_template("result.html", num_pos = result_pos, num_neg = result_neg, name_text = name)
##name을 db에 저장하고 받는 절차가 필요함 지금은 단순히 모듈안에서 저장만 했다.
# dt.del_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)