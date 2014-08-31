# -*- coding: utf-8 -*-

'''
Author : Dhruv Choudhary
https://github.com/choudharydhruv/Coursolve
SQL file genrating script for understanding Collaboration in a MOOC
'''
import json
import sys
import google
from google import search
import wikipedia
import re
import cPickle as pickle
import string
import sys
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import csv
import sqlite3 as lite

def get_wiki_category(skill):
    return skill 

def processSkills(skills):
    skillList=[]
    for s in skills:
        s = s.replace('\t',',').lower()
        s = s.replace('/',',')
        s = s.replace(' AND ',',')
        s = s.replace(' And ',',')
        s = s.replace(' and ',',')
        s = s.replace('basic','')
        s = s.replace('fundamentals','')
        s = s.replace(' & ',',')
        s = s.replace('expert',' ')
        s = s.lower().strip()
        for k in s.split(","):
            skillList.append(k)
    return skillList
    
def handle_disambiguation(name, excep):
    urls = search(name)
    while True:
        try:
            url = urls.next()
	    if (url.find('wikipedia') !=-1):
                subterms = re.split("/", url)
                wiki_name = subterms[len(subterms)-1]
	except:
	    print "Cannot find wiki page for this term, putting as Unknown ", name
	    return 'Unknown'
	    

def get_wiki_url(term):
    try:
        urls = search(str(term)+' wikipedia')
	#results = wikipedia.search(term)
        #except wikipedia.exceptions.DisambiguationError as e:
	#print e.options
	while True:
	    try:
	        url = urls.next()
	    except:
		print "Cannot find wiki page for this term, putting as Unknown ", term
		return '','Unknown'
	    #print url, url.find('wikipedia')
	    if (url.find('wikipedia') !=-1):
		#print "Found Wikipedia page ", url
                subterms = re.split("/", url)
		#print subterms
                wiki_name = subterms[len(subterms)-1]
		#try:
		#    wikipedia.summary(wiki_name)
		#except wikipedia.exceptions.DisambiguationError as e:
		#    wiki_name = handle_disambiguation(wiki_name, e)
	        #print "Url and term: ", url, term, wiki_name
		break
    except ValueError:
        print "Error in google query for term: ", term
        url = ''
        wiki_name = ""
        #exit(0)
    return url,wiki_name

def remove_misspell_synonyms(skills, synonym):
    histTerm = {}

    #Collect all skills in a dictionary
    dictionary = {}
    for s in skills:
        for k in s:
	    key = (k.lower().lstrip(" "))
	    if (key != ''):
                try:
                    dictionary[key] += 1
                except KeyError:  
                    dictionary[key] = 1

    #for d in dictionary.keys():
    #    print d,dictionary[d] 

    for skill in dictionary.keys():
	try:
	    name = synonym[skill]
	except KeyError:
            url, name = get_wiki_url(skill)
	    print "Wikipedia entry for ", skill, " is ", name, url
	    synonym[skill] = name
	    #exit(0)
        try:
	    histTerm[name] += dictionary[skill]
	except KeyError:
	    histTerm[name] = dictionary[skill]

    #for d in histTerm.keys():
    #    print d, histTerm[d] 

    askills = []
    for a in skills:
	user = []
        for i in a:
	    key = (i.lower().lstrip(" "))
	    try:
	        user.append(synonym[key])
	    except:
	        user.append(u'Unknown')
		print "Appending unknown for ", i
		exit(0)
	askills.append(user)

    return askills, synonym, histTerm

def extractRecFromJson(dataset):

    data = json.load(dataset) 

    con = lite.connect('collaboration.db')

    cur = con.cursor()

    cur.execute("""DROP TABLE IF EXISTS USERS """)
    cur.execute("CREATE TABLE USERS ( \
        USR_ID char(64) NOT NULL PRIMARY KEY, \
        GENDER varchar(50), \
        EMPLOYM varchar(1000),\
        EDU_HGHST varchar(1000),\
        TIME_LST_ACCESS DATETIME, \
        LOCATION varchar(1000),\
        LOGIN_NUM number, \
        BIRTH_YR number)")
    cur.execute("CREATE TABLE SKILLS_ACQ (\
        USR_ID char(64) NOT NULL, \
        SKILL varchar(1000) NOT NULL,\
        PRIMARY KEY (USR_ID, SKILL))")
    cur.execute("CREATE TABLE SKILLS_DES (\
        USR_ID char(64) NOT NULL,\
        SKILL varchar(1000) NOT NULL,\
        PRIMARY KEY (USR_ID, SKILL))")
    cur.execute("CREATE TABLE SUBSCR_FORUM (\
        USR_ID char(64) NOT NULL,\
        NEED_ID char(64) NOT NULL,\
        PRIMARY KEY (USR_ID, NEED_ID))")
    cur.execute("CREATE TABLE SUBSCR_THREADS (\
        USR_ID char(64) NOT NULL,\
        NEED_ID char(64) NOT NULL,\
        THREAD_IDN number NOT NULL,\
        FOREIGN KEY(USR_ID) REFERENCES USERS(USR_ID),\
        FOREIGN KEY(THREAD_IDN) REFERENCES THREADS(THREAD_IDN),\
        PRIMARY KEY(USR_ID, NEED_ID, THREAD_IDN) )")
    cur.execute("CREATE TABLE COMMENTS_NEED (\
        USR_ID char(64) NOT NULL, \
        NEED_ID char(64) NOT NULL,\
        TIME_COMM DATETIME NOT NULL,\
        FOREIGN KEY(USR_ID) REFERENCES USERS(USR_ID) )")
    cur.execute("CREATE TABLE REQ_JOIN_NEED (\
        USR_ID char(64) NOT NULL,\
	NEED_ID  char(64) NOT NULL,\
	CRS_PRJ_ID char(64) NOT NULL,\
	VOTES_NUM number,\
	RESCINDED varchar(50),\
	TIME_REQ_JOIN DATETIME NOT NULL,\
        FOREIGN KEY(USR_ID) REFERENCES USERS(USR_ID),\
        PRIMARY KEY (USR_ID, NEED_ID, TIME_REQ_JOIN) )")
    cur.execute("CREATE TABLE JOIN_NEED (\
	USR_ID char(64) NOT NULL,\
	NEED_ID char(64) NOT NULL,\
	VOTES_NUM number,\
	TIME_JOIN DATETIME,\
        FOREIGN KEY(USR_ID) REFERENCES USERS(USR_ID),\
        PRIMARY KEY (USR_ID, NEED_ID) )")
        #--TYPE post or reply. Reply have repl_num = 0 reply_to_id null if post
        #-- post nmr unique within the thread
    cur.execute("CREATE TABLE POSTS (\
	POST_IDN  number,\
	THREAD_IDN number,\
	USR_ID char(64) NOT NULL,\
	NEED_ID char(64) NOT NULL,\
	REPLY_TO_ID number,\
	LIKES_NUM number,\
	TIME_POST DATETIME,\
	REPL_NUM number,\
	TYPE   varchar(50),\
        PRIMARY KEY(POST_IDN, THREAD_IDN),\
        FOREIGN KEY(THREAD_IDN) REFERENCES THREADS(THREAD_IDN),\
        FOREIGN KEY(USR_ID) REFERENCES USERS(USR_ID)   )")

        #-- threads should be unique in the system
    cur.execute("CREATE TABLE THREADS  (\
	THREAD_IDN number NOT NULL,\
	TIME_LST DATETIME,\
	USR_ID char(64) NOT NULL,\
	USR_ID_LST char(64),\
	NEED_ID char(64) NOT NULL,\
	POSTS_NUM number,\
	VIEWS_NUM number,\
	TIME_THR DATETIME,\
	PRIMARY KEY(THREAD_IDN),\
        FOREIGN KEY(USR_ID) REFERENCES USERS(USR_ID)   )")

    for entry in data.items():
        dt = (entry[1]['Last Access Time']).split('.')
        if dt[0] == None:
	    datetime = "NULL"
	else:
	    datetime = dt[0]
	#print datetime
        cur.execute('''INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?)''',(entry[0], (entry[1]['Gender']).lower(), (entry[1]['Employment']).lower(), (entry[1]['Highest Education']).lower(), datetime, (entry[1]['Location']).lower(), entry[1]['Num Logins'], entry[1]['Year of Birth']))

    ids = []
    askills = []
    dskills = []
    for entry in data.items():
        ids.append(entry[0]) 
        askills.append(processSkills(entry[1]['Acquired Skills']))
        dskills.append(processSkills(entry[1]['Desired Skills']))

    wikipedia.set_lang("en")
    try:
        synonym = pickle.load(open( "data/synonyms.p", "rb" ) )
    except:
        print "no synonym.p file, building synonyms from scratch..."
	synonym = {}
    askills, synonym, unique_askills = remove_misspell_synonyms(askills, synonym)
    dskills, synonym, unique_dskills = remove_misspell_synonyms(dskills, synonym)
    print "Writing back synonyms file"
    pickle.dump( synonym, open( "data/synonyms.p", "wb" ) )

    for i,sk in enumerate(askills):
	unique_sk = []
        for s in sk:
            if s not in unique_sk:
                unique_sk.append(s)
        for s in unique_sk:
            tline = [ids[i], s]
	    #print tline     
            cur.execute('''INSERT INTO SKILLS_ACQ VALUES(?,?)''', (ids[i], s) )

    for i,sk in enumerate(dskills):
	unique_sk = []
        for s in sk:
            if s not in unique_sk:
                unique_sk.append(s)
        for s in unique_sk:
            tline = [ids[i], s]
	    #print tline     
            cur.execute('''INSERT INTO SKILLS_DES VALUES(?,?)''', (ids[i], s) )


    for entry in data.items():
	nids = entry[1]['Forum Subscriptions']
	unique_need = []
        for n in nids: 
	    #print entry[0],n
	    if n['need'] not in unique_need:
	        unique_need.append(n['need'])
                cur.execute('''INSERT INTO SUBSCR_FORUM VALUES(?,?)''', (entry[0], n['need']) )

    for entry in data.items():
	tids = entry[1]['Forum Thread Subscriptions']
	unique_tids = []
	for t in tids:
            if t not in unique_tids:
                unique_tids.append(t)
	        #print entry[0], t['need'], t['thread']
                cur.execute('''INSERT INTO SUBSCR_THREADS VALUES(?,?,?)''', (entry[0], t['need'], t['thread']) )

    for entry in data.items():
	tcom = entry[1]['Need Comments']
	unique_comms = []
	for t in tcom:
            if t not in unique_comms:
                dt = (t['timestamp']).split('.')
                if dt[0] == None:
	            time = "NULL"
	        else:
	            time = dt[0]
                unique_comms.append(t)
	        #print entry[0], t['need'], time
                cur.execute('''INSERT INTO COMMENTS_NEED VALUES(?,?,?)''', (entry[0], t['need'], time) )

    for entry in data.items():
        req = entry[1]['Need Join Requests']
	unique_entry = []
        for r in req:
	    dtime = r['timestamp'].split('.')
	    if dtime[0] == None:
	        time = "NULL"
	    else:
	        time = dtime[0]
	    i = [entry[0], r['need'], time]
	    if i not in unique_entry:
	        unique_entry.append(i)
                #print entry[0], r['need'], r['course_project'], r['num_votes'], r['rescinded'], time
                cur.execute('''INSERT INTO REQ_JOIN_NEED VALUES(?,?,?,?,?,?)''', (entry[0], r['need'], r['course_project'], r['num_votes'], r['rescinded'], time  ) )

    for entry in data.items():
        req = entry[1]['Need Joins']
	unique_entry = []
        for r in req:
            dtime = r['timestamp'].split('.')
            if dtime[0] == None:
	        time = "NULL"
	    else:
	        time = dtime[0]
	    i = [entry[0], r['need'], time]
	    if i not in unique_entry:
	        unique_entry.append(i)
                #print entry[0], r['need'], time
                cur.execute('''INSERT INTO JOIN_NEED VALUES(?,?,?,?)''', (entry[0], r['need'],  r['num_votes'], time) )

    for entry in data.items():
        req = entry[1]['Forum Posts/Replies']
	unique_posts = []
        for r in req:
	    p = [r['id'], r['thread']]
	    if p not in unique_posts:
                unique_posts.append(p)
		parent_id = r['parent_post']
		if parent_id == None:
		    parent_id = "NULL"
		if (parent_id is not "NULL") and (r['reply_count'] == 0):
		    post_type = u'REPLY'
		else:
		    post_type = u'POST'
	        dtime = r['timestamp'].split('.')
                if dtime[0] == None:
	            time = "NULL"
	        else:
	            time = dtime[0]
	        #print r['id'], r['thread'], entry[0], r['need'], parent_id, r['likes'], time, r['reply_count'], post_type
                cur.execute('''INSERT INTO POSTS VALUES(?,?,?,?,?,?,?,?,?)''', (r['id'], r['thread'], entry[0], r['need'], parent_id, r['likes'], time, r['reply_count'], post_type) )


    for entry in data.items():
        thr = entry[1]['Forum Threads']
	unique_thr = []
        for r in thr:
	    if r['id'] not in unique_thr:
                unique_thr.append(r['id'])
		ltime = r['last_updated_time'].split('.')
                if ltime[0] == None:
	            last_time = "NULL"
	        else:
	            last_time = ltime[0]
		stime = r['timestamp'].split('.')
                if stime[0] == None:
	            start_time = "NULL"
	        else:
	            start_time = stime[0]
		#print r['id'], last_time, entry[0], r['last_updated_user'], r['need'], r['post_count'], r['view_count'], start_time
		cur.execute('''INSERT INTO THREADS VALUES(?,?,?,?,?,?,?,?)''', (r['id'], last_time, entry[0], r['last_updated_user'], r['need'], r['post_count'], r['view_count'], start_time ) )







    con.commit()
    return   

if __name__ == '__main__':
    dataset = open(sys.argv[1])
   # sys.stdout.buffer.write(chr(9986).encode('utf8'))

    extractRecFromJson(dataset)

