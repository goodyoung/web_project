import sqlite3
import pandas as pd
from dbconnect import DBUpdater

dn = DBUpdater()

# 사용자 LIST 반환
def userNameList():
    dn = DBUpdater()
    dfUser= dn.select_table('User')
    li = dfUser['Name'].to_list()
    return li

# 투표 LIST 반환
def voteNameList():
    dn = DBUpdater()
    dfVoteName = dn.select_table('VoteName')
    li = dfVoteName['Name'].to_list()
    return li

# voteID에 따른 투표 조항 반환
def voteItem(voteName):
    dn = DBUpdater()
    
    dfVoteName = dn.select_table('VoteName')
    dfVoteItem = dn.select_table('VoteItem')
    
    #result = dfVoteName[dfVoteName['Name'] == voteName]['Name'].values[0]
    voteID = dfVoteName[dfVoteName['Name'] == voteName]['ID'].values[0]
    
    result = dfVoteItem[dfVoteItem['VoteID'] == voteID]['Name'].to_list()

    # return voteID, result
    return result

# 허가받은 User 반환
def acceptUser(userName):
    dn = DBUpdater()
    DfName = dn.select_table('User')
    userList = DfName['Name'].to_list()
    
    if userName in userList:
        print(userName)
    else:
        print('관리자의 허가가 필요합니다.')
    # return ?
    
# Vote ID 와 그에 따른 투표 조항 반환_ type tuple
def itemCollect(articleNum):
    dn = DBUpdater()
    dfVoteItem = dn.select_table('VoteItem')
    
    voteItemNum = dfVoteItem[dfVoteItem['Name'] == articleNum]['Num'].values[0]
    voteID = dfVoteItem[dfVoteItem['Name'] == articleNum]['VoteID'].values[0]
    
    return voteID, voteItemNum


# DPUpdater에 있는 insert_VoteResult 재반환
def userVote(userID, voteID, articleNumv):
    dn = DBUpdater()
    dn.insert_VoteResult(userID, voteID, articleNumv)
    
    
# 입력받은 건의 사항 저장
def receivePropsal(proposal):
    dn = DBUpdater()
    dn.insert_value('listable', '건의', proposal)  
    
    
"""
def voteResult(bla):
    dn = DBUpdater()
    dfVoteItem = dn.select_table('VoteItem')
    dfVoteResult = dn.select_table('VoteResult')
    # dfItem = dfItem[dfItem['VoteID'] == bla]
    
    return
""" 

'''

def vote_result(vote_item_id):
    db = DBUpdater()
    df_item = db.select_table('VoteItem')
    df_result = db.select_table('VoteResult')
    df_item = df_item[df_item['VoteID']==vote_item_id]
    # merge할 때 VoteID도 함께 고려해야 할 듯??
    
    tot = pd.merge(df_result,df_item[['Num','Name']],on = 'Num',how = 'outer')
    tot_result = tot.groupby('Name')['UserID'].count().to_dict()
    tot_dict = {}
    # VoteID는 1로 임의로 지정해 두었다.
    for i in df_item['Name']:
        tot_dict[i]= tot_result[i]

    return tot_dict
    '''

# 입력받은 건의 사항 저장
def receivePropsal(proposal):
    dn = DBUpdater()
    dn.insert_value('listable', '건의', proposal)  




