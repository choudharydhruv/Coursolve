# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 11:19:04 2014
Modified on Aug 3
@author: Elena Tomás
"""

import numpy as np
import pandas as pd
import os
import re, string
import json
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import time
from nltk.stem import porter
import nltk
import operator
from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from nltk.corpus import stopwords
import igraph
import google
from igraph.remote import gephi
import csv
import cPickle as pickle
import os
import sys


"""
To run in the command line: python netword_skills.py <folder name>

To load the pickle dictionary (acquired)
H=igraph.Graph.Read_Pickle(fname=folder+'/graph_pickle.p')
"""

#skills = pd.read_json("/home/elena/Coursolve/skills_ds_need.txt")

def build_hier_dic(word,dic,count):
    """Build dictionary of skills based on wikipedia categories up until 3 ascendents"""
    while count<3:
        result=get_category(word)
        dic[word]=result
        count+=1
        for item in result:
            if item not in dic.keys():
                build_hier_dic(item,dic,count)    

    return dic

def clean_dic(dic):
    """This dictionary eliminates duplicity {A:B,B:A}"""    
    newdict={}
    for key,value in dic.items():
        if len(value)==1:
            try:
                newdict[value[0]]="".join(dic[value[0]])
            except KeyError:
                newdict[key]=value
    delkey=None
    for key in newdict.keys():
        if newdict[key] in newdict.keys():
            delkey=key
            del newdict[key]
    newdict={}
    
    for key in dic.keys():
        if key != str(delkey):
            newdict[key]=dic[key] 
    return newdict
    
def build_hier_list(dic):
    links=[]
    for key in dic:
        for item in dic[key]:
            pair=(key,item)
            links.append(pair)
    return links

def set_parents(links):
    temp=np.transpose(links)
    set1=set(temp[0])
    set2=set(temp[1])
    children = list(set1.difference(set2))
    parent = list(set2.difference(set1))
    intersect = list(set2.intersection(set1))
    return parent
            
    


    
def get_category(word,page=""):
    
    print "Getting categories for the skill ...", word
    stop = stopwords.words('english')
    exclude = set(string.punctuation)
    if page=="":
        
        page='http://en.wikipedia.org/wiki/'+str(word)
        page=re.sub(" ","_",page)   
    else:
        page=page
    c=urlopen(page) #soup=BeautifulSoup(urlopen(page+str(word)))
    soup=BeautifulSoup(c.read())
    categories={}
    b=soup.findAll('a', {'title' : re.compile("^Category:*")})#    abstract=soup.find('div',id="bodyContent").p.getText()
    items= soup.find('div',id="bodyContent").findAll('p')
    abstract=""
    for item in items:
        abstract+= item.getText()
    for cat in b:
        try:
            key=re.sub(re.compile('Category:'),"",cat['title']).lower()
            keylist=key.split(" ")
            keylist=[item for item in keylist if item not in stop and item not in exclude] #           
            key=" ".join(keylist)#            key = ' '.join(ch for ch in s if ch not in exclude)
            if len(keylist)<5:
                categories[key]=0 
                for bigram in nltk.bigrams(key.split(" ")):
                    big=" ".join(bigram)  
                    categories[big]=0
        except KeyError:
            continue
 
        
    for key in categories.keys():
        try:
            is_cat=re.findall(key.lower(),abstract.lower())
            categories[key]+=len(is_cat)
        except:
            continue
  
    for key in categories.keys():
        if categories[key] <2:
            del categories[key]

    for key in categories.keys():
        if categories[key] == list(key):
            categories[key]=""
            
    for key in categories.keys():            
        if len(nltk.word_tokenize(key))>2:
            for bigram in nltk.bigrams(nltk.word_tokenize(key)):
                big=" ".join(bigram)
                try:
                    if categories[big]:
                        del categories[big]
                except:
                    print "key",big,"was not deleted"
                    
    for key in categories.keys():
        if key.lower()==str(word).lower():
            value=categories[key]
            del categories[key]
            
    if len(categories)==0:
        categories[word]=""
        return categories.keys()
        

#        desambiguate(word)
#        temp = raw_input("What is the skill you are looking for? Or press 0 for None ")
#        if temp=="0":
#            categories[word]=""
#            exit
#        else:            
#            print "You entered..." , temp
#            get_category(str(temp))
    return categories.keys()

def get_json_data(jsonfile):
    
    """
    Loads json file and returns a data frame with user id, acquired_skills, desired_skills , location, gender and employment.
    """
    
    data = json.load(open(jsonfile, 'r')) 
    ncol=len(data[data.keys()[0]].keys())+1   
    colnames=[re.sub(" ","_",x).lower() for x in data[data.keys()[0]].keys()]
    nrow=len(data.keys())
    columns=['id']+colnames
    data_skills = pd.DataFrame(np.ones([nrow,ncol],dtype='str'),columns=columns)
    for i in range(len(data.keys())):
        idn=data.keys()[i]
        data_skills.id.ix[i]=idn
        for j in data[data.keys()[i]].keys():
            colname=re.sub(" ","_",j).lower()
            try:
                data_skills[str(colname)].ix[i]=data[str(idn)][j].lower()
            except:
                data_skills[str(colname)].ix[i]=data[str(idn)][j]

    return data_skills
    
    
def get_skills_list(df,column='desired_skills',employment='',location='',gender=''):
    
    """
    Loads skills dataframe and process desired_skills or acquired_skills to return
    a dictionary with all the possible skills for a given location, gender and employment
    """
    
    skills_dict={}
    if (location!=''):
        df=df[df['location']==location.lower()]
    if (employment!=''):
        df=df[df['employment']==employment.lower()]
    if (gender!=''):
        df=df[df['gender']==gender.lower()]
        
    for index, row in df.iterrows():
        for item in row[column]:#            skills_dict[item]+=1
            for term in re.split(",",item):
                try:
                    term=str(term.lower().lstrip(" "))
                    skills_dict[term]+=1
                except KeyError:
                    skills_dict[term]=1
    return skills_dict

def get_stem_skills_list(dic):
    
    """
    Stems the skills dictionary 
    """
    
    skills_dict={}
        
    stemmer=porter.PorterStemmer()
    list_keys=[nltk.word_tokenize(k) for k in dic.keys()]
    stem_keys=[]
    stem_keys0=dic.keys()
    
    for item in list_keys:
        item_keys=[stemmer.stem(k) for k in item]
        stem_keys.append( "_".join(item_keys))
        
    for i in range(len(stem_keys)):
        item = stem_keys[i]
        try:
            skills_dict[item]+=dic[stem_keys0[i]]
        except KeyError:
            skills_dict[item]=dic[stem_keys0[i]]
    
    return skills_dict
    
def top_skills(skills_dict,n=10):
    
    """
    Plots the n most popular skills for a given skills dictionary
    """
    top_list= sorted(skills_dict, key=skills_dict.get, reverse=True)[:n]
    top={}

    for item in top_list:
        top[item]=skills_dict[item]
    

    top_list=sorted(top.values())
    top_key_list2d= sorted(top.iteritems(), key=operator.itemgetter(1))
    top_key=[]
    for item in  top_key_list2d:
        top_key.append(item[0])
    
    plt.figure()    
    plt.bar(range(len(top)), top_list,align='center')
    plt.xticks(range(len(top)), top_key,rotation=90)
    plt.subplots_adjust(bottom=0.3)
    plt.show()
    return top

import urllib



def showfirst(phrase):
    
    """
    Returns the url and word of the first entry after a google search of the word + wikipedia
    """    
    try:
      urls=google.search(phrase)
      url=urls.next()
      words=re.split("/",url)
      word=words[len(words)-1]
      word=re.sub("_"," ",word)
    except:
        print "Error searching the word", phrase , "in Google"
        url=""
        word=""
    return url, word

          
      
def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G



def make_graph(link_list):
    G = dict()
    for n1, n2 in link_list:
        make_link(G, n1, n2)
    return G
      

def make_link2(G, node1, node2,val):
    if node1 not in G:
        G[node1] = {}
    try:
        (G[node1])[node2] =  val
    except KeyError:
        (G[node1])[node2] = val
    if node2 not in G:
        G[node2] = {}
    try:
        (G[node2])[node1] =  val
    except KeyError:
        (G[node2])[node1] = val
    return G

def make_graph2(link_list,link_val):
    G = dict()
    count=0
    for n1, n2 in link_list:
        make_link2(G, n1, n2,link_val[count])
        print n1,n2
        count+=1
    return G
    

    
def clean_list(lists):
    
    """
    Eliminates duplicities from the category list.
    """    
    for item in lists:
        if item[0]==item[1]:
            print "Removing duplicate",item
            lists.remove(item)
    return lists


def build_synonyms_dic(wlist,dic):
    
    """
    Converts skill into a synonym skill eliminating mispellings.It returns two dictionaries,
    one with the new dictionary and other with a translating dictionary.
    """    
    newdic={}
    transdic={}
    for word0 in wlist:
        value=dic[word0]
        print "Processing skill...", word0,value
        result=showfirst(str(word0)+" wikipedia")
        word=result[1]
        newword=re.sub(" - Wikipedia, the free encyclopedia","",result[1]).lower()
        print "Converting to skill...", newword,value

        newword_list.append(newword)
        page=result[0]
        try:
            newdic[newword]+=value
        except KeyError:
            newdic[newword]=value
        transdic[word0]=newword
    return newdic,transdic
    
def export_dic(dic,f):
    with open(f+(".p"),'wr') as dicf:
        pickle.dump(dic,dicf)
    with open(f+(".json"),'wr') as dicf:
        json.dump(dic,dicf)

def import_dic(f):
    with open(f+(".p"),'rb') as dicf:
        dic=pickle.load(dicf)
        return dic

def exportGraph(graph,f):
    
    """
    Converts igraph to a nodes and edges csv files.
    """    
    g1=open(f+("/nodes.csv"),'wr')
    g2=open(f+("/edges.csv"),'wr')
    writerg1 = csv.writer(g1)
    writerg1.writerow(["id","Label","Value","Color"])
    writerg2 = csv.writer(g2)
    writerg2.writerow(["Source","Target"])
    edges=graph.get_edgelist()
    for i in range(len(graph.vs)):
        writerg1.writerow([i, graph.vs[i]['label'],graph.vs[i]['value'],graph.vs[i]['color']])
        print i, graph.vs[i]['label'],graph.vs[i]['value'],graph.vs[i]['color']
    for item in edges:
        writerg2.writerow([item[0],item[1]])
        print i,item[0],item[1]
    
    
  
if __name__ == "__main__":
    
    nodes=[]
    exclude=[]
    print str(sys.argv[1])
    try:
        folder=str(sys.argv[1])
    except:
        print "No folder was passed as argument"
        folder="/home/elena/Desktop/p"

    print "Folder..",folder
    skills=get_json_data(str(folder)+"/skills_ds_need.txt")
#    desired_dic=get_skills_list(skills,column='desired_skills',location='united states',gender='female',employment='employed')
    acquired_dic=get_skills_list(skills,column='acquired_skills',location='spain',gender='female',employment='employed')
#    desired_dic=get_skills_list(skills,column='desired_skills')
#    acquired_dic=get_skills_list(skills,column='acquired_skills')

    dic=acquired_dic
    
    word_list=dic.keys()
##
    sk=[]
    skval=[]
    newword_list=[]
    newword_dic={}
    transword_dic={}

    f=open(str(folder)+"/acquired_skills_tree.txt",'wr')    
    fname=str(folder)+"/transword_dic_acquired"
    fname2=str(folder)+"/newdic_acquired"
    
    newword_dic,transword_dic=build_synonyms_dic(word_list,dic)
    export_dic(transword_dic,fname)
    export_dic(newword_dic,fname2)    
#
#
    for word in newword_dic.keys():
        dic={}
        value=newword_dic[word]
        newword=re.sub(" - Wikipedia, the free encyclopedia","",word)
        count=0
        dic=build_hier_dic(newword,dic,count)
        lista0=build_hier_list(dic)
        lista=clean_list(lista0)
        print lista
        sk+=lista
        skval+=list(np.ones(len(lista))*value)
    listadic=make_graph2(sk,skval)

    value = [sum(listadic[newword].values()) for newword in listadic.keys()]
    
    H=igraph.Graph()
    H.add_vertices(listadic.keys())
    H.add_edges(sk)
    H.vs['label']=H.vs['name']
    cl_blue = colors.colorConverter.to_rgb('blue')
    cl_red = colors.colorConverter.to_rgb('red')
    col=np.ones(len(H.vs),dtype=str)
    col=[cl_blue for item in col]
    val=np.ones(len(H.vs),dtype=str)
    val=[None for item in val]
    H.vs['color']=col
    H.vs['value']=val
    H.vs['size']=1.
    for i in range(len(H.vs)):
        if (H.vs['name'][i].lower() in newword_dic.keys()):
            print H.vs[i]['color'],i,H.vs['name'][i].lower() 
            H.vs[i]['color'] = cl_red
            H.vs[i]['value']=newword_dic[H.vs['name'][i]]
            H.vs[i]['size']=H.vs[i]['size']+H.vs[i]['size']**2*0.5*H.vs[i]['value']/sum(newword_dic.values())
    igraph.plot(H)
    H.write_gml(folder+'/graph_glm.txt')
    H.write_pickle(folder+'/graph_pickle.p')
    exportGraph(H,folder)



