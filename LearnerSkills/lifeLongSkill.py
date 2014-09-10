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

def group_skills(skill_dic):
    for sk in skill_dic:
        category_list = get_wiki_category(sk)

def build_users_graph(skills, unique_skills):
    print "Building graph edges"
    
    nodes_csv = open('nodes.csv', 'w')
    edges_csv = open('edges.csv', 'w')
    nptr = csv.writer(nodes_csv, delimiter= ',')
    eptr = csv.writer(edges_csv, delimiter= ',')

    nptr.writerow(['ID', 'Label'])
    eptr.writerow(['Source', 'Target', 'Type', 'Weight'])

    graph_id = 0
    graph_id_map = {}
    for i in range(0, len(skills)):
        for j in range(i+1, len(skills)):
	    overlap = 0
            for a in skills[i]:
                if a in skills[j]:
	            overlap += 1.0 
	    if overlap>0:
	        overlap = overlap / (len(skills[i]) + len(skills[j]) - overlap)
	    #print skills[i]
	    #print skills[j]
	    #print overlap
	    if overlap>0.15:
		src=0
		dest = 0
		if i not in graph_id_map:
		    graph_id +=1
		    graph_id_map[i] = graph_id
		    src = graph_id
	            nptr.writerow([src,src])
		else:
		    src = graph_id_map[i]
		if j not in graph_id_map:
		    graph_id +=1
		    graph_id_map[j] = graph_id
		    dest = graph_id
	            nptr.writerow([dest,dest])
		else:
		    dest = graph_id_map[j]
	        eptr.writerow([src, dest, 'Undirected', overlap])
	        print "Calculating skill overlap between users", src,dest,overlap
		print skills[i],skills[j] 

def build_skills_graph(skills, unique_skills):

    G=nx.Graph()

    print "Building graph edges"
    skill_list = unique_skills.keys()

    d2_dict = defaultdict(dict)    

    nodes_csv = open('nodes.csv', 'w')
    edges_csv = open('edges.csv', 'w')
    nptr = csv.writer(nodes_csv, delimiter= ',')
    eptr = csv.writer(edges_csv, delimiter= ',')

    nptr.writerow(['ID', 'Label'])
    eptr.writerow(['Source', 'Target', 'Type', 'Weight'])

    graph_id_map = {}
    
    for sk in skills:
        for a in range(0,len(sk)):
            for b in range(a+1,len(sk)):
	        try:
		    d2_dict[sk[a]][sk[b]] += 1.0
		except:
		    try:
		        d2_dict[sk[b]][sk[a]] += 1.0
		    except:
		        d2_dict[sk[a]][sk[b]] = 1.0

    graph_id = 0
    for i in range(1, len(skill_list)):
        for j in range(1,len(skill_list)):
            if i==j:
                continue
	    try:
		common = d2_dict[skill_list[i]][skill_list[j]]
		union = unique_skills[skill_list[i]] + unique_skills[skill_list[j]] - common
	        if union>10 and common>1 and unique_skills[skill_list[j]]>5 and unique_skills[skill_list[i]]>5:
                    jaccard = common/union
	        else:
		    jaccard = 0.0
	        if (jaccard >= 0.1):
	            G.add_edge(skill_list[i],skill_list[j],weight=jaccard)
	            print "Added link between ", skill_list[i], skill_list[j], jaccard, common, union
		    src=0
		    dest = 0
		    if i not in graph_id_map:
			graph_id +=1
			graph_id_map[i] = graph_id
			src = graph_id
	                nptr.writerow([src,(skill_list[i]).encode("utf-8")])
		    else:
			src = graph_id_map[i]
		    if j not in graph_id_map:
			graph_id +=1
			graph_id_map[j] = graph_id
			dest = graph_id
	                nptr.writerow([dest,(skill_list[j]).encode("utf-8")])
		    else:
			dest = graph_id_map[j]
		    eptr.writerow([src, dest, 'Undirected', jaccard])
            except:
		continue

    '''	   
    for i in range(1, len(skill_list)):
        for j in range(i+1,len(skill_list)):
	    common = 0.0
            union = 0.0 
	    for sk in skills:
		if skill_list[i] in sk and skill_list[j] in sk:
		    common += 1
		if skill_list[i] in sk or skill_list[j] in sk:
		    union += 1
	    if union > 10:
                jaccard = common/union
	    else:
		jaccard = 0.0
	    if (jaccard > 0.01):
	        #d2_dict[skill_list[i]][skill_list[j]] = jaccard
	        G.add_edge(skill_list[i],skill_list[j],weight=jaccard)
	        print "Added link between ", skill_list[i], skill_list[j], jaccard,common, union
    '''

    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.4]
    emedium=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <0.4 and d['weight'] >0.2]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.2]

    pos=nx.spring_layout(G) # positions for all nodes
    print "Drawing nodes..."

    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=10)

    # edges
    nx.draw_networkx_edges(G,pos,edgelist=elarge,width=6)
    nx.draw_networkx_edges(G,pos,edgelist=emedium,width=4,alpha=0.5,edge_color='g')
    nx.draw_networkx_edges(G,pos,edgelist=esmall,width=1,alpha=0.5,edge_color='b',style='dashed')

    # labels
    #nx.draw_networkx_labels(G,pos,font_size=5,font_family='sans-serif')

    plt.axis('off')
    #plt.savefig("weighted_graph.png") # save as png
    plt.show() # display






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
    #print "Original skills list ", skillList
    #for t in skillList:
    #    print (t.lower().strip())
    return skillList
    
def handle_disambiguation(name, excep):
    #print excep.options()
    #print wikipedia.summary(excep.options[0])
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
    ids = []
    askills = []
    dskills = []
    gender = []
    location = []
    employment = []
    rec = json.load(dataset)
    for entry in rec.items():
	#print "User entry ", entry
        ids.append(entry[0]) 
        askills.append(processSkills(entry[1]['Acquired Skills']))
        dskills.append(processSkills(entry[1]['Desired Skills']))
        gender.append(entry[1]['Gender'])
        location.append(entry[1]['Location'])
        employment.append(entry[1]['Employment'])

    wikipedia.set_lang("en")

    try:
        synonym = pickle.load(open( "data/synonyms.p", "rb" ) )
    except:
        print "no synonym.p file, building synonyms from scratch..."
	synonym = {}
 
    askills, synonym, unique_askills = remove_misspell_synonyms(askills, synonym)
    dskills, synonym, unique_dskills = remove_misspell_synonyms(dskills, synonym)

    #print "Writing back synonyms file"
    #pickle.dump( synonym, open( "synonyms.p", "wb" ) )

    #print "Writing back unique Acquired skills histogram file"
    #pickle.dump( unique_askills, open( "unique_askills.p", "wb" ) )

    #print "Writing back unique Desired skills histogram file"
    #pickle.dump( unique_askills, open( "unique_dskills.p", "wb" ) )

    comb_skills = []
    for i,j in zip(askills,dskills):
        user = []    
        for s in i:
            user.append(s)
        for s in j:
	    if s not in user:
                user.append(s)
        comb_skills.append(user)

    tskills = []
    for i in askills:
        user = []
        for s in i: 
	    if s not in user:
	        user.append(s)
        tskills.append(user)
    askills = tskills

    build_skills_graph(askills, unique_askills)
    #build_users_graph(askills,unique_askills)

    return ids,askills,dskills,gender,location,employment   

if __name__ == '__main__':
    dataset = open(sys.argv[1])
   # sys.stdout.buffer.write(chr(9986).encode('utf8'))

    ids,askills,dskills,gender,loc,emp = extractRecFromJson(dataset)
