from flask import Flask, render_template, request, redirect, url_for
import pymysql 

conn = pymysql.connect(host = "localhost", user="root", passwd="", db ="free_board", charset = "utf8")
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    sql_query = "SELECT * FROM board ORDER BY num DESC "
    cur.execute(sql_query)
    

    data_list = cur.fetchall() 
    return render_template('index.html', data_list = data_list)

@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/write_action', methods=['POST'])
def write_action():
    title = request.form.get('title')
    writer = request.form.get('writer')
    content = request.form.get('content')

    sql = "INSERT INTO board (title, writer, content, views) VALUES (%s, %s, %s, 0)"
    values = (title, writer, content)
    cur.execute(sql, values)
    conn.commit()

    return go_main()     

def go_main() :
    return redirect(url_for("index"))


@app.route('/content/<int:num>')
def content(num):
    sql = "UPDATE board SET views = views + 1 WHERE num = %s"
    values = num
    cur.execute(sql, values)
    conn.commit()

    sql = "SELECT * FROM board WHERE num = %s"
    cur.execute(sql, values)
    data_list = cur.fetchall()
    return render_template('content.html', data_list = data_list)


@app.route('/content/<int:num>edit/<num>')
def edit() :
    sql = "UPDATE board SET views = views + 1 WHERE num = %s"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  

