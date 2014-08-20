# -*- coding: utf-8 -*-

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

    user = csv.writer(open("users.csv", "wb"))
    for entry in data.items():
        tline = [ entry[0], (entry[1]['Gender']).lower(), (entry[1]['Employment']).lower(), (entry[1]['Highest Education']).lower(), entry[1]['Last Access Time'], (entry[1]['Location']).lower(), entry[1]['Num Logins'], entry[1]['Year of Birth']  ]
	#print tline
	user.writerow(tline)


    ids = []
    askills = []
    dskills = []
    ask = csv.writer(open("data/skills_acq.csv", "wb")) 
    dsk = csv.writer(open("data/skills_des.csv", "wb")) 
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
        for s in sk:
            tline = [ids[i], s]
	    print tline     
	    ask.writerow(tline) 

    for i,sk in enumerate(dskills):
        for s in sk:
            tline = [ids[i], s]
	    print tline     
	    ask.writerow(tline) 

    return ids,askills,dskills,gender,location,employment   

if __name__ == '__main__':
    dataset = open(sys.argv[1])
   # sys.stdout.buffer.write(chr(9986).encode('utf8'))

    ids,askills,dskills,gender,loc,emp = extractRecFromJson(dataset)
