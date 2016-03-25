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

f3 = open("posT.txt",'r')
f4 = open("negT.txt",'r')

for l in f3:
  poskeywords.append(l[:-1])
for l in f4:
  negkeywords.append(l[:-1])

knnpos = []
knnneg = []

pos = Set()
neg = Set()
maxp = 10
maxn = 10

supply=[]


#sprint(randint(0,9))

unlabel= []
label = []
test = []
i=0
for l in f1:
  if(i<10200):
    unlabel.append(l)
  i+=1

i=0
for l in f2:
  if(i<10200):
    label.append(l)
  else:
    test.append(l)
  i+=1

#print label


var = []
def addPosKeywords(index):
  tokens = we.make_token(label[index][1:])
  l = Set()
  for t in tokens:
    if t in poskeywords:
      l.add(t)
  if(len(l)!=0):
    knnpos.append(l)
  return l

def addNegKeywords(index):
  tokens = we.make_token(label[index][1:])
  l = Set()
  for t in tokens:
    if t in negkeywords:
      l.add(t)
  if(len(l)!=0):
    knnneg.append(l)
  return l

#print test
def testModel():
  acc=0
  for t in test:
    tokens = we.make_token(t[1:])
    prob = knn.knnclassifier(knnpos,knnneg,tokens.keys(),5)
    if((prob[1]>prob[0])==(t[0]=="1") or (prob[0]>prob[1])==(t[0]=="0")):
      acc = acc+1
  return (acc/462.0)*100

index = 0
while(maxp>0):
  if label[index][0] == "1":
    maxp -=1
    tokens = we.make_token(label[index][1:])
    l = Set()
    for t in tokens:
      if t in poskeywords :
        pos.add(t)
        l.add(t)
    if(len(l)!=0):
      knnpos.append(l)
  index+=2

index = 1
while(maxn>0):
  if label[index][0] == "0":
    maxn -=1
    tokens = we.make_token(label[index][1:])
    l = Set()
    for t in tokens:
      if t in negkeywords :
        neg.add(t)
        l.add(t)
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
for i in range(200,10200):
  active=0
  index = i
  if(i%1000==0):
    print "at i",i,"used set",extra,testModel()
  tokens = we.make_token(label[index][1:])
  bayesprob = bayes.bayesianClassifier(pos,neg,tokens.keys())
  knnprob = knn.knnclassifier(knnpos,knnneg,tokens.keys(),5)
  if((bayesprob[1]>=bayesprob[0] and knnprob[1]<=knnprob[0]) or (bayesprob[1]<=bayesprob[0] and knnprob[1]>=knnprob[0])):
    active=1
    #print label[index][:-1]
    #print tokens.keys().
  #else:
    #print bayesprob,knnprob
  if(bayesprob[-1]==0 or knnprob[-1]==0 or active==1 ):
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
