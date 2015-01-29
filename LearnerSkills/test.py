# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl
import json
import string

from string import punctuation
import re

import datetime
from dateutil.parser import parse

import nltk
from nltk.stem import porter

X = np.random.randint(0,9,size=(10))
Y = np.random.randint(0,9,size=(10))

print X,Y
print np.dot(X.T, X)/X.shape[0]

R = ( ((X-X.mean(0))*(Y-Y.mean(0)) ).sum() / (X.std(0)*Y.std(0)) )
R = R/X.shape
print R

#To calculate R between different variables
print np.corrcoef(X,Y)


#Plotting points
pl.figure(1)
pl.subplot(2,1,1)
pl.plot(X,Y, 'ro')

X = 100*np.random.randn(1000)+ 25

#Plotting histograms
pl.subplot(2,1,2)
pl.hist(X, 50)
pl.xlabel('Random vector')
pl.ylabel('Frequencies')
#pl.show()


pl.figure(2)
X = np.random.randint(0,9,size=(10))
Y = np.random.randint(0,9,size=(10))
Z = np.random.randint(0,50,size=(10))
C = np.random.randint(0,9,size=(10))
pl.scatter(X,Y,Z**2,C)
#pl.show()

#Opening a json file
try:
    with open('a.txt') as cFile:
        data = json.load(cFile)
    #if converting json string
    response = json.loads(data)
except:
    print "No file"

#removing punctuation form words
s1 = "This is smart!"
exclude = set(string.punctuation)
s = ''.join(ch for ch in s1 if ch not in exclude)
print s1,s
# Other sets are string.digits string.whitespaces string.lowercase string.uppercase

#Converting to lower case, upper case
print s.lower(), s.upper()


#Concatenating items in a list
l = ['this', 'i  s', 'a', 'ball']
s = ' '.join(l)
print l,s

for word in s.split(' '):
   if word: # empty strings are falsy by default
       print word.strip()

#Python strings are immutable
s = s.replace('this', 'that')
print s

#Sorting a dictionary based on the value
d = {}
d['abc'] = 9
d['xyz'] = 5
d['thh'] = 8

for w in sorted(d, key = d.get, reverse=True):
  print w,d[w]

#####################Regular expressions################################
l =['dog dart','vi484hhd is','3434jkkjk','dfkdfh86768','wedge']
s = ' '.join(l)

#splitting at occurence of pattern
print s, re.split("\W+",s)  
#splits at start of non words

#Splitting on 1 or more a characters
print re.split("[a-f]+",'0a3aB9', flags=re.IGNORECASE)

#Two words starting with d
r = re.search("(d\w+).*(d\w+).*",s) 
print r.group()

#if no match return value is None
r = re.search(".*\d$",s)
if r is None:
    print "No match"

#Looking for a word following a hiphen
m = re.search("(?<=-)\w+","fhhfh-kdfnkne")
print m.group()  # prints kdfnkne

#Return all non overlapping sequences of pattern as a list
m = re.findall("[dp]\w+", "dog is in the park")
print m   # prints ['dog', 'park']

#Replacing unwanted characters in a string
s = ' in this / string 345/ $ i . dont know what {to} say'
rx=re.compile('(\W+)') #removes all non word characters
s = rx.sub(' ',s).strip()
print s


#############################################################

#String formatting
print 'x: {0[0]} y={0[0]} ',format((3,5))

#Parsing dates

d = datetime.datetime.strptime("2015-10-09T19:00:55Z","%Y-%m-%dT%H:%M:%SZ")
print d.date(), d.time()

#Using porter stemmer
l =['dog dart','dolls','3434jkkjk','dfkdfh86768','wedge\'s']
stemmer = porter.PorterStemmer()
lnew = [stemmer.stem(k) for k in l]
print lnew  

#csv reading writing
import csv

lines = csv.reader(open('tmp.csv',"rb"))
data = list(lines)
#print data[:5]

with open('tmp.csv',"rb") as csvfile:
    lines = csv.reader(csvfile, delimiter = ',', )


#json to pandas
'''
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
'''

#pandas
import pandas as pd
colnames = ['x'+str(i) for i in range(9)]
colnames = colnames+['y']
print colnames
reader = pd.read_csv('tmp.csv',names=colnames)
#print reader[['x1','x2']]

print reader.groupby('x1').sum().index
print reader.groupby('x1').sum().values
#Use size() instead of sum if u dont need to sum



