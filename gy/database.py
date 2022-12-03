import sqlite3
import pandas as pd
name_list=[]
def database(num_pos=0,num_neg=0):
    conn = sqlite3.connect('./database/vote_base.db')
    sql = 'SELECT * FROM Vote'
    POS = int(num_pos)
    NEG = int(num_neg)
    if (num_pos == 0) & (num_neg == 0):
        pass
    else:
        conn.execute(f"INSERT INTO Vote VALUES ({POS},{NEG})") # row값 추가

    # INSERT INTO VoteName VALUES (2,'a');
    df = pd.read_sql(sql, conn)
    pos_num = df.sum(axis= 0)[0]
    neg_num = df.sum(axis= 0)[1]
    conn.commit()
    conn.close()
    return pos_num,neg_num 

def del_database():
    conn = sqlite3.connect('./database/vote_base.db')
    conn.execute(f"DELETE FROM Vote") # table delete 
    conn.commit()
    conn.close()

def commit_name(user_name=0):
    global name_list
    if user_name:
        name_list.append(user_name)
    else:
        pass
    return name_list[0]