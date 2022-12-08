from dbconnect import DBUpdater
import database as db

a = db.vote_name()
print(a)

dn = DBUpdater()
b = dn.select_table('VoteName')
print(b['Name'].to_list())