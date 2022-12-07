import sqlite3
import pandas as pd
from dbconnect import DBUpdater
db = DBUpdater()

def vote_name():
    db = DBUpdater()
    df_name = db.select_table('VoteName')
    ui = df_name['Name'].to_list()
    return ui
    
def vote_item(vote_name):
    db = DBUpdater()
    print(db)
    df_name = db.select_table('VoteName')
    df_vote_item = db.select_table('VoteItem')
    vote_item_id = df_name[df_name['Name'] == vote_name]['ID'].values[0]
    result_name = df_vote_item[df_vote_item['VoteID'] == vote_item_id]['Name'].to_list()
    print('난 여기 있어용요용용',vote_item_id)
    
    return result_name, vote_item_id
    
    
    
def name_collect(user_name):
    db = DBUpdater()
    df_name = db.select_table('User')
    ret1 = df_name['Name'] == user_name
    
    if len(df_name[ret1]) <=0:
        #유저 리스트에 포함이 안된 사람들
        print('관리자의 허가가 필요합니다.')
        return 
    else:
        user_id = df_name.loc[df_name['Name'] ==user_name,'ID'].values[0]
        return user_id

def item_collect(item):
    db = DBUpdater()
    df_item = db.select_table('VoteItem')
    voteItemNum = df_item[df_item['Name'] == item]['Num'].values[0]
    voteID = df_item[df_item['Name'] == item]['VoteID'].values[0]
    #투표항목을 정하고 투표를 하기 때문에
    #여기선 투표항목이 오류날 경운 없으므로 오류처리 X
    return voteItemNum, voteID
        
def user_vote(voteID,user_id,voteItemNum):
    db = DBUpdater()
    db.insert_VoteResult(voteID, user_id, voteItemNum)
    return 


def vote_result(vote_item_id):
    db = DBUpdater()
    df_item = db.select_table('VoteItem')
    df_result = db.select_table('VoteResult')
    df_item = df_item[df_item['VoteID']==vote_item_id]
    #merge할 때 VoteID도 함께 고려해야 할 듯??
    
    tot = pd.merge(df_result,df_item[['Num','Name']],on = 'Num',how = 'outer')
    tot_result = tot.groupby('Name')['UserID'].count().to_dict()
    tot_dict = {}
    #VoteID는 1로 임의로 지정해 두었다.
    for i in df_item['Name']:
        tot_dict[i]= tot_result[i]

    return tot_dict
        
        
        
        
    