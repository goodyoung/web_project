import pandas as pd
import sqlite3, time
from datetime import datetime

class DBUpdater:  
    def __init__(self):
        """생성자: SQLDB 연결 생성"""
        self.conn = sqlite3.connect('./vote_base.db')
        self.db_create()
        self.tableList = ['User', 'VoteName', 'VoteItem', 'VoteResult',"Board"]
        # self.codes = {}
        # self.get_comp_info()

    def __del__(self):
        """소멸자: SQLDB 연결 해제"""
        self.conn.close()
        
    def db_create(self):
        sql = """
        CREATE TABLE IF NOT EXISTS "Board" (
            "id"	INTEGER NOT NULL,
            "writer"	TEXT,
            "title"	TEXT NOT NULL,
            "content"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        )
        """
        self.conn.execute(sql)
        
        # User
        sql = """
        CREATE TABLE IF NOT EXISTS "User" (
            "ID"	INTEGER NOT NULL,
            "Name"	TEXT NOT NULL,
            PRIMARY KEY("ID")
        )
        """
        self.conn.execute(sql)
        
        # VoteName
        sql = """
        CREATE TABLE IF NOT EXISTS "VoteName" (
            "ID"	INTEGER NOT NULL,
            "Name"	TEXT NOT NULL,
            PRIMARY KEY("ID" AUTOINCREMENT)
        )
        """
        self.conn.execute(sql)
        
        # VoteItem
        sql = """
        CREATE TABLE IF NOT EXISTS "VoteItem" (
            "VoteID"	INTEGER NOT NULL,
            "Num"	INTEGER NOT NULL,
            "Name"	TEXT NOT NULL,
            PRIMARY KEY("VoteID","Num")
        )
        """
        self.conn.execute(sql)
        
        # VoteResult
        sql = """
        CREATE TABLE IF NOT EXISTS "VoteResult" (
            "VoteID"	INTEGER,
            "UserID"	INTEGER,
            "Num"	INTEGER
        )
        """
        self.conn.execute(sql)
        self.conn.commit()

    def reset_db(self):
        try:
            for table in self.tableList:
                sql = f"drop table if exists {table}"
                self.conn.execute(sql)
            self.conn.commit()
            self.db_create()
        except:
            print('reset_table Error')

    def reset_table(self, table_name=None):
        try:
            if table_name == None:
                for table in self.tableList:
                    sql = f"DELETE FROM {table}"
                    self.conn.execute(sql)
            else:
                sql = f"DELETE FROM {table_name}"
                self.conn.execute(sql)
            self.conn.commit()
        except:
            print('reset_table Error')

    def convert_value(self, values=None):
        print(values)
        try:
            if isinstance(values,str):
                x = '\"'+ values+'\"'
                print(x)
                return x
            res_ls = []
            for v in values:
                if isinstance(v, int) or isinstance(v, float):
                    res_ls.append(str(v))
                elif isinstance(v, str):
                    res_ls.append(f'\"{v}\"')
            res = ", ".join(res_ls)
            # print(res)
            return res
        except:
            print('convert_value Error')
            
    def convert_columns(self, columns=None):
        try:
            if isinstance(columns,str):
                return columns
            cols = ",  ".join(columns)
            return cols
        except:
            print('convert_columns Error')

    def insert_value(self, table_name=None, columns=None, values=None):
        try:
            cols = self.convert_columns(columns)
            vals = self.convert_columns(values)
            print(vals)
            if isinstance(vals,str):
                vals = '\"'+ vals+'\"'
            print(vals)
            sql = f"INSERT INTO {table_name} ({cols}) VALUES ({vals})"
            print(sql)
            self.conn.execute(sql)
            self.conn.commit()

        except:
            print('insert_value Error')

    def insert_VoteName(self, name):
        try:            
            sql = f"INSERT INTO VoteName (Name) VALUES (\"{name}\")"
            print(sql)
            self.conn.execute(sql)
            self.conn.commit()
            
        except:
            print('insert_VoteName Error')

    def insert_VoteItem(self, voteID, num, name):
        VoteName_df = self.select_table('VoteName')
        VoteItem_df = self.select_table('VoteItem')
        # print(VoteName_df['ID'].values)
        # print(VoteItem_df['Num'].values)
        # print(voteID, num, name)
        if voteID in VoteName_df['ID'].values:
            if num in VoteItem_df['Num'].values:
                print('이미 있다')
            else:
                try:
                    sql = f"INSERT INTO VoteItem (VoteID, Num, Name) VALUES ({voteID}, {num}, \"{name}\")"
                    self.conn.execute(sql)
                    self.conn.commit() 
                except:
                    print('insert_VoteItem Error')
        else:
            print('존재하지 않은 voteID')
            


    def insert_VoteResult(self, voteID, userID, voteItemNum):
        VoteItem_df = self.select_table('VoteItem')
        User_df = self.select_table('User')
        VoteResult_df = self.select_table('VoteResult')
        # print(VoteName_df['ID'].values)
        # print(VoteItem_df['Num'].values)
        # print(voteID, num, name)
        check = len(VoteItem_df[(VoteItem_df['VoteID'] == voteID) & (VoteItem_df['Num'] == voteItemNum)])
        # print(check)
        # print(VoteItem_df[VoteItem_df['VoteID'] == voteID])
        # print(VoteItem_df[VoteItem_df['Num'] == voteItemNum])
        # print(VoteItem_df[(VoteItem_df['VoteID'] == voteID) & (VoteItem_df['Num'] == voteItemNum)])
        if check > 0:
            pass
        else:
            print('존재하지 않은 voteID, voteItem')
            return
        
        cond_1 = VoteResult_df['VoteID'] == voteID
        cond_2 = VoteResult_df['UserID'] == userID
        
        if len(VoteResult_df[cond_1 & cond_2]) > 0:
            print('이미 투표 하셨습니다.')
            return
            
        
        if userID in User_df['ID'].values:
            try:
                sql = f"INSERT INTO VoteResult (VoteID, UserID, Num) VALUES ({voteID}, {userID}, {voteItemNum})"
                self.conn.execute(sql)
                self.conn.commit() 
            except:
                print('insert_VoteResult Error')
        else:
            print('존재하지 않은 userID')
        



    # def insert_VoteResult(self, voteID, userID, voteItemNum):
    #     try:
    #         sql = f"INSERT INTO VoteResult (VoteID, UserID, Num) VALUES ({voteID}, {userID}, {voteItemNum})"
    #         self.conn.execute(sql)
    #         self.conn.commit() 
    #     except:
    #         print('insert_VoteResult Error')
    

    def insert_Board(self, writer, title, content):
        try:            
            sql = f"INSERT INTO Board (writer, title, content) VALUES (\"{writer}\", \"{title}\", \"{content}\")"
            print(sql)
            self.conn.execute(sql)
            self.conn.commit()
            
        except:
            print('insert_Board Error')
    

            
    def select_table(self, table_name, columns=None):
        try:
            if columns==None:
                cols = "*"
            else:
                cols = self.convert_columns(columns)
            
            sql = f"SELECT {cols} FROM {table_name}"
            df = pd.read_sql(sql, self.conn)
            return df
        except:
            print('select_table Error')       
    
    
    def sql_input(self, sql):
        try:
            sql = sql
            self.conn.execute(sql)
            self.conn.commit()
        except:
            print('sql_input Error')




if __name__ == "__main__":
    print("dbconect.py 실행")
    x = DBUpdater()
    # print(x.select_table('User'))
    x.__del__