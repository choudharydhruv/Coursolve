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

import scipy.cluster.vq as vq

cent, label = vq.kmeans2(X,k)


#Adding column of 1s
a = np.random.rand((5,5))
b = np.ones((5,6))
b[:,1:] = a

print a,b

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

#pandas to numpy
ar = np.array(df['x1'])
df = pd.DataFrame(ar,columns=['x1'])
df = ps.concat([df1,df2], axis=1)


df.fillna('')

#libsvm 3.12 wierd rules
from svm import *
from svmutil import *
px= svm_problem(Y,Data.tolist())
m = svm_train(px, '-t 2 -c 10')
labels,_,_ = svm_predict(Y_val, Data_val.tolist(), m)


"""
...
'options':
    -s svm_type : set type of SVM (default 0)
        0 -- C-SVC
        1 -- nu-SVC
        2 -- one-class SVM
        3 -- epsilon-SVR
        4 -- nu-SVR
    -t kernel_type : set type of kernel function (default 2)
        0 -- linear: u'*v
        1 -- polynomial: (gamma*u'*v + coef0)^degree
        2 -- radial basis function: exp(-gamma*|u-v|^2)
        3 -- sigmoid: tanh(gamma*u'*v + coef0)
        4 -- precomputed kernel (kernel values in training_set_file)
    -d degree : set degree in kernel function (default 3)
    -g gamma : set gamma in kernel function (default 1/num_features)
    -r coef0 : set coef0 in kernel function (default 0)
    -c cost : set the parameter C of C-SVC, epsilon-SVR, and nu-SVR (default 1)
    -n nu : set the parameter nu of nu-SVC, one-class SVM, and nu-SVR (default 0.5)
    -p epsilon : set the epsilon in loss function of epsilon-SVR (default 0.1)
    -m cachesize : set cache memory size in MB (default 100)
    -e epsilon : set tolerance of termination criterion (default 0.001)
    -h shrinking : whether to use the shrinking heuristics, 0 or 1 (default 1)
    -b probability_estimates : whether to train a SVC or SVR model for probability estimates, 0 or 1 (default 0)
    -wi weight : set the parameter C of class i to weight*C, for C-SVC (default 1)
    -v n: n-fold cross validation mode
    -q : quiet mode (no outputs)
"""


