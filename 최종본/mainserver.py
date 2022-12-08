from flask import Flask, render_template, redirect, url_for, jsonify

import sqlite3
import pandas as pd
from flask import request
from flask_admin import Admin
import module.database as dt

app = Flask(__name__)
#메인
###################################################################################
@app.route('/')
def main():
    return render_template('thumbnail.html')
###################################################################################

#건의
###################################################################################
conn = sqlite3.connect('./vote_base.db')
cur = conn.cursor()
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
    return redirect(url_for("proposal"))    

@app.route('/format', methods=['GET'])
def delete_community():
    conn = sqlite3.connect('./vote_base.db')
    cur = conn.cursor()
    sql = "DELETE FROM board WHERE id >= 1"
    cur.execute(sql)
    conn.commit()
    
    sql = '''
    UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'Board' 
    '''
    cur.execute(sql)
    conn.commit()
    
    return render_template('board.html')

###################################################################################

#투표
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
        try:
            result = request.form.to_dict()
            user_id = dt.name_collect(result['name'])
            result_name, fo = dt.vote_item(result['vote'])
            return redirect(url_for('index', result_name= result_name, user_id =user_id))
        except:
            return render_template('test.html', menu_list = lis)  
    else:
        return render_template('menu.html', menu_list = lis) 
    
@app.route('/vote/<result_name>/<int:user_id>',methods=['GET','POST'])
def index(result_name,user_id):
    # post로 받기 위해 tem를 index.html에 넘겨 form action을 실행 시키려고
    tem1,tem2 = result_name, user_id
    if request.method == 'POST':
        result = request.form.to_dict()
        #getlist의 길이가 2개로 제한 해야 중복 투표 막는다. 한번만 투표 하게 하려고 나중에 처리 하자
        voteItemNum, voteID = dt.item_collect(result['items'])
        # user_id = dt.name_collect(result['name'])
        #user의 투표한 결과 값을 db에 저장한다.
        dt.user_vote(voteID,user_id,voteItemNum)
        return render_template("result.html")
    else:
        tot_name = result_name[1:-1].replace('\'','').split(',')
        for k,i in enumerate(tot_name):
            tot_name[k] = i.strip()
        return render_template('index.html', result_name = tot_name, test = tem1, ids = tem2)

@app.route("/resulttot",methods=['GET','POST'])
def result3():
    #투표 항목을 불러온다.
    lis = dt.vote_name()
    if request.method == 'POST':
    #투표 결과를 불러온다.
        select_name = request.form.to_dict()['vote']
        result_name, vote_item_id = dt.vote_item(select_name)
        
        tem = dt.vote_result(vote_item_id)
        return render_template("resulttot.html", s = tem)
    else:
        return render_template('resulttot_test.html', menu_list = lis)   
###################################################################################

#관리자
###################################################################################
@app.route('/admins')
def admin():
    
    return render_template('admin.html')

@app.route('/admin/add')
def admin_add():
    return render_template('adminAdd.html')

@app.route('/admin/add/result', methods =['GET','POST'])
def hi():
    if request.method == 'POST':
        tt = request.form.to_dict()
        votename = tt['voteName'].split(',')[0]
        voteitem = tt['voteArticle'].split(',')
        print(votename,voteitem)
        dt.admin_vote(votename,voteitem)
        return render_template('rere.html')
    else:
        return render_template('adminAdd.html')
###################################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)    
    