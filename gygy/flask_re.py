from flask import Flask, render_template, redirect, url_for, jsonify

import sqlite3
import pandas as pd
import database as dt   # database 모듈화
from flask import request

app = Flask(__name__)
@app.route('/vote/<result_name>&user_id=<user_id>',methods=['GET','POST'])
def index(result_name,user_id):
    # post로 받기 위해 tem를 index.html에 넘겨 form action을 실행 시키려고
    tem = result_name
    if request.method == 'POST':
        print(request.method)
        result = request.form.to_dict()
        # print(request.form.getlist)
        #getlist의 길이가 2개로 제한 해야 중복 투표 막는다. 한번만 투표 하게 하려고 나중에 처리 하자
        voteItemNum, voteID = dt.item_collect(result['select1'])
        print(voteItemNum,'voteid임돵',voteID)
        # user_id = dt.name_collect(result['name'])
        
        print('uwer',user_id)
        #user의 투표한 결과 값을 db에 저장한다.
        dt.user_vote(voteID,user_id,voteItemNum)
        return redirect(url_for('userresult'))
    
    else:
        print(request.method)
        print('용용',user_id)
        tot_name = result_name[1:-1].replace('\'','').split(',')
        for k,i in enumerate(tot_name):
            tot_name[k] = i.strip()
        return render_template('index.html', result_name = tot_name, test = tem)
    

@app.route('/vote2/',methods=['GET'])
def vote2():
        return {'list':['item1','item2']}
    
@app.route('/menu',methods=['GET','POST'])
def menu():
    #투표 항목을 불러온다.
    lis = dt.vote_name()
    if request.method == 'POST':
        print('asg',request.method)
        result = request.form.to_dict()
        user_name = result['name']
        vote_name = result['vote']
        print(user_name, vote_name)
        user_id = dt.name_collect(user_name)
        result_name, fo = dt.vote_item(vote_name)
        print('user_id이에용',user_id)
        #fo 는 버리는 변수
        
        return redirect(url_for('index', result_name= result_name, user_id = user_id))
    #url_for안에 함수 이름인지 라우트 경로인지 잘 모르겠다.
    else:
        print('lis임도ㅓ',lis)
        return render_template('menu.html', menu_list = lis)    
    


    
#checkbox에서 
# name : 전달할 값의 이름이다.
# value : 전달될 값이다.

@app.route("/userresult",methods=['GET','POST'])
def userresult():
    return render_template("result.html")
##name을 db에 저장하고 받는 절차가 필요함 지금은 단순히 모듈안에서 저장만 했다.
# dt.del_database()


# @app.route("/resulttot",methods=['GET'])
# def result2():
#     tem = dt.vote_result()
#     print('tem입니당',tem)
    
#     return render_template("resulttot.html", s = tem)


@app.route("/resulttot3",methods=['GET','POST'])
def result3():
    #투표 항목을 불러온다.
    lis = dt.vote_name()
    if request.method == 'POST':
    #투표 결과를 불러온다.
        print(request.form.to_dict())
        select_name = request.form.to_dict()['select1']
        
        result_name, vote_item_id = dt.vote_item(select_name)
        
        tem = dt.vote_result(vote_item_id)
        
        return render_template("resulttot.html", s = tem)
    else:
        return render_template('resulttot_test.html', menu_list = lis)    




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)