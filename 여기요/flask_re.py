from flask import Flask, render_template, redirect, url_for, jsonify

import sqlite3
import pandas as pd
from flask import request, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


import database as dt
from dbconnect import DBUpdater 

dn = DBUpdater()
conn = sqlite3.connect('./vote_base.db')
cur = conn.cursor()


app = Flask(__name__)
@app.route('/')
def main():
    return render_template('thumbnail.html')


###################################################################################
app.config
app.config['FLASK_ADMIN_SWATCH'] = 'slate'
admin = Admin(app, name='AdminPage', template_mode='bootstrap3')

###################################################################################

@app.route('/pro')
def proposal():
    conn = sqlite3.connect('./vote_base.db')
    cur = conn.cursor()
    
    sql = '''
    SELECT * FROM board ORDER BY id DESC;
    '''
    cur.execute(sql)
    dfs = cur.fetchall()

    return render_template('board.html', dfs = dfs )

@app.route('/content/<int:id>')
def content(id):
    conn = sqlite3.connect('./vote_base.db')
    cur = conn.cursor()

    sql = f"SELECT * FROM board WHERE id = {id}"
    cur.execute(sql)
    data_list = cur.fetchall()
    
    print(data_list)
    return render_template('content.html', data_list = data_list)

@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/write_action', methods=['POST'])
def write_action():
    conn = sqlite3.connect('./vote_base.db')
    cur = conn.cursor()
    
    title = request.form.get('title')
    writer = request.form.get('writer')
    content = request.form.get('content')
    
    sql = f"INSERT INTO Board (title, writer, content) VALUES (\"{title}\", \"{writer}\", \"{content}\")"
    cur.execute(sql)
    conn.commit()
    
    return go_main()     

def go_main() :
    return redirect(url_for("proposal"))

###################################################################################


@app.route('/addList', methods=['GET','POST'])

def add():
    if request.method == 'POST':
        result = request.form.to_dict() 
        proposal = result['prop']
        dt.receiveProposal(proposal)
        return render_template('end.html')
    else:
        return render_template('proposal.html')

@app.route('/menu',methods=['GET','POST'])
def menu():
    #투표 항목을 불러온다.
    lis = dt.vote_name()
    if request.method == 'POST':
        result = request.form.to_dict()
        user_id = dt.name_collect(result['name'])
        result_name, fo = dt.vote_item(result['vote'])
        #fo는 버리는 변수
        return redirect(url_for('index', result_name= result_name, user_id =user_id))
    else:
        return render_template('menu.html', menu_list = lis) 

@app.route('/vote/<result_name>/<int:user_id>',methods=['GET','POST'])
def index(result_name,user_id):
    # post로 받기 위해 tem를 index.html에 넘겨 form action을 실행 시키려고
    tem1,tem2 = result_name, user_id
    if request.method == 'POST':
        result = request.form.to_dict()
        # print(request.form.getlist)
        #getlist의 길이가 2개로 제한 해야 중복 투표 막는다. 한번만 투표 하게 하려고 나중에 처리 하자
        voteItemNum, voteID = dt.item_collect(result['select1'])
        print(voteItemNum,'voteid임돵',voteID)
        # user_id = dt.name_collect(result['name'])
        print('uwer',user_id)
        #user의 투표한 결과 값을 db에 저장한다.
        dt.user_vote(voteID,user_id,voteItemNum)

        return render_template("result.html")
    
    else:
        print('user_id입니당',user_id)
        tot_name = result_name[1:-1].replace('\'','').split(',')
        for k,i in enumerate(tot_name):
            tot_name[k] = i.strip()
        return render_template('index.html', result_name = tot_name, test = tem1, ids = tem2)

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
 
    
'''@app.route('/vote2/',methods=['GET'])
def vote2():
        return {'list':['item1','item2']}'''    

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


    # admin.add_view(ModelView(User, db.session))