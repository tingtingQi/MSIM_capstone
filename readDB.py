import MySQLdb as mdb
import sys
import numpy as np
import re

con = mdb.connect(host = 'localhost', user = 'root', passwd = "123", db = "capstone") 
cur = con.cursor() # the cursor object will let you execute all the queries you need

# return the number of unique users
query1 = "SELECT * FROM users"
cur.execute(query1)
# store number of users from users id count
user_num =  cur.rowcount
user_id = [] # array of all user id
rows = cur.fetchall()
for row in rows:
    user_id.append(row[0])
# print user_id
# print "number of users: ",user_num

def find_userid_index(this_user_id):
    """
    find the user id index (natural number)
    """
    return user_id.index(this_user_id)
# print find_userid_index('58518963-b814-4df9-a49d-03900a2a839b')

query2 = "SELECT * FROM technologies"
cur.execute(query2)
# store number of technologies from technology id count
technology_num = cur.rowcount
technology_id = [] # array of all user id
rows = cur.fetchall()
for row in rows:
    technology_id.append(row[0])
# print "number of technologies: ", technology_num
# print technology_id

def find_techid_index(this_tech_id):
    """
    find the technology id index (natural number)
    """
    return technology_id.index(this_tech_id)
# print find_techid_index(23)

query3 = "SELECT * FROM keywords"
cur.execute(query3)
# store all the keywords
keywords = []
rows = cur.fetchall()
for row in rows:
    keywords.append(row[0])
# print keywords[7421]

# rows = cur.fetchall()
# for row in rows:
#     for col in row:
#         print col
#     print "\n"

query4 = "SELECT * FROM technology_keywords"
cur.execute(query4)
technology_keywords = {}
rows = cur.fetchall()
for row in rows:
    if row[1] not in technology_keywords:
        technology_keywords[row[1]] = []
        technology_keywords[row[1]].append(row[0])
    else:
        technology_keywords[row[1]].append(row[0])
# print technology_keywords



def technology_vector(keywords, technology_id):
    """
    given keywords (id) list and some specific technology_id, return a technology keywords 0-1 mapping list
    """
    this_keywords = technology_keywords[technology_id] # access all keywords for this technology
    index_dict = dict((value, idx) for idx, value in enumerate(keywords))
    index_list = [index_dict[x] for x in this_keywords] # return the index list of this_keywords in the full list of keywords
    this_allkeywords = np.zeros(len(keywords))  # initialize the list with all value 0, and set 
    this_allkeywords[index_list] = 1
    print this_allkeywords
# np.set_printoptions(threshold='nan') # show all values in array when it is too long
# np.array(technology_vector(keywords, 2)) # test technology_vector function


def technology_user_score(user_num, technology_num):
    """
    given the total number of users and technologies, return the score matrix. ongoing.
    """
    score = np.zeros((user_num, technology_num)) # initiate the 2darray
    query5 = "SELECT user_id, details FROM user_activities"
    cur.execute(query5)
    rows = cur.fetchall()
    for row in rows: # only for "content_view"
        user_id = row[0]
        userid_index = find_userid_index(user_id)
        detail = rows[1][0]
        # print detail
        start_index = detail.find("Article_id") # finding start from "Article_id"
        technology_id = int(re.search('\d+', detail[start_index:]).group(0)) # return the first matched group -- technilogy id for this user
        techid_index = find_techid_index(technology_id) # change technology id into natural number
        score[userid_index, techid_index] += 1 # change 1 according to weight
    print score
# np.set_printoptions(threshold='nan') # show all values in array when it is too long
technology_user_score(user_num, technology_num)