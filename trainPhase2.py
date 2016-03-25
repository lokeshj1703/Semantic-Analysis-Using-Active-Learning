import nltkwordextraction
import activeBayesianClassifier as bayes
import os,sys
from random import randint
import wordextractor as we
from sets import Set
import activeknn as knn

f1 = open("Data/unlabeled.txt",'r')
f2 = open("Data/labeled.txt",'r')

poskeywords = []
negkeywords = []
pos = {}
neg = {}
posl=0
negl=0

f3 = open("posT.txt",'r')
f4 = open("negT.txt",'r')

for l in f3:
  pair = l.split()
  poskeywords.append(pair[0])

for l in f4:
  pair = l.split()
  negkeywords.append(pair[0])

knnpos = []
knnneg = []

maxp = 10
maxn = 10

supply=[]


#sprint(randint(0,9))

unlabel= []
label = []
test = []
i=0
for l in f1:
  if(i<7000):
    unlabel.append(l)
  i+=1

i=0
for l in f2:
  if(i<7000):
    label.append(l)
  else:
    test.append(l)
  i+=1

#print label


var = []
def addPosKeywords(index):
  global posl
  tokens = we.make_token(label[index][1:])
  l = []
  for t in tokens:
    if t in poskeywords:
      if(pos.has_key(t)):
        pos[t]+=1
      else:
        pos[t]=1
      posl+=1
      l.append(t)
  if(len(l)!=0):
    knnpos.append(l)
  return l

def addNegKeywords(index):
  global negl
  tokens = we.make_token(label[index][1:])
  l = []
  for t in tokens:
    if t in negkeywords:
      if(neg.has_key(t)):
        neg[t]+=1
      else:
        neg[t]=1
      negl+=1
      l.append(t)
  if(len(l)!=0):
    knnneg.append(l)
  return l

#print test
def testModel():
  acc=0
  for t in test:
    tokens = we.make_token(t[1:])
    testlabel = knn.knnclassifier2(knnpos,knnneg,tokens.keys(),5)
    if((testlabel==1)==(t[0]=="1") or (testlabel==0)==(t[0]=="0")):
      acc = acc+1
#    else:
 #     print t
  #    print we.tagged_tokens(t[1:])"""
  return (acc/3662.0)*100

index = 0
while(maxp>0):
  if label[index][0] == "1":
    maxp -=1
    tokens = we.make_token(label[index][1:])
    l = []
    for t in tokens:
      if t in poskeywords :
        if(pos.has_key(t)):
          pos[t]+=1
        else:
          pos[t]=1
        posl+=1
        l.append(t)
    if(len(l)!=0):
      knnpos.append(l)
  index+=2

index = 1
while(maxn>0):
  if label[index][0] == "0":
    maxn -=1
    tokens = we.make_token(label[index][1:])
    l = []
    for t in tokens:
      if t in negkeywords :
        if(neg.has_key(t)):
          neg[t]+=1
        else:
          neg[t]=1
          negl+=1
        l.append(t)
    if(len(l)!=0):
      knnneg.append(l)
  index+=2

print len(pos)
print len(neg)
#print knnpos
i=0
acc = 0
"""while(i<100):
  index = randint(0,10661)
  tokens = we.make_token(label[index][1:])
  prob = knn.knnclassifier(knnpos,knnneg,tokens.keys(),5)
  if(prob[-1]==1):
    i = i+1
    print (prob[1]>prob[0]),label[index][0]
    if((prob[1]>prob[0])==(label[index][0]=="1") or (prob[0]>prob[1])==(label[index][0]=="0")):
      acc = acc+1
print acc"""
extra = 0
dump = 0
print pos,neg,testModel()
for i in range(20,7000):
  active=0
  index = i
  if(i%1000==0):
    print "at i",i,"used set",extra,testModel()
  tokens = we.make_token(label[index][1:])
  bayeslabel = bayes.bayesianClassifier2(pos,neg,posl,negl,tokens.keys())
  knnlabel = knn.knnclassifier2(knnpos,knnneg,tokens.keys(),5)
  if((bayeslabel==1 and knnlabel==0) or (bayeslabel==0 and knnlabel==1)):
    active=1
    #print label[index][:-1]
    #print tokens.keys().
  #else:
    #print bayesprob,knnprob
  if(bayeslabel==-1 or knnlabel==-1 or active==1 ):
    if(label[index][0]=="1"):
      l = addPosKeywords(index)
    else:
      l = addNegKeywords(index)
    #print l
    if len(l)==0:
      dump+=1
      #print we.tagged_tokens(label[index][1:])
    else:
      extra+=1
#print pos
#print neg
print extra,dump
