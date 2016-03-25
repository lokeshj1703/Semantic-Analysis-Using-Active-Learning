import nltkwordextraction as nl
import os,sys
import wordextractor as we
from sets import Set
import math

posfile = open("posT.txt",'w')
negfile = open("negT.txt",'w')

f1 = open("Data/unlabeled.txt",'r')
f2 = open("Data/labeled.txt",'r')

pos={}
neg={}
N=10662
nt = {}
for l in f2:
  taggedTokens = we.tagged_tokens(l[1:])
  for t in taggedTokens:
    if((t[1][0]=="J" and t[1][1]=="J") or (t[1][0]=="R" and t[1][1]=="B")):
      if(nt.has_key(t[0])):
        nt[t[0]]+=1
      else:
        nt[t[0]]=1
      if(l[0]=="1"):
        if(pos.has_key(t[0])):
          pos[t[0]]+=1
        else:
          pos[t[0]]=1          
      else:
        if(neg.has_key(t[0])):
          neg[t[0]]+=1
        else:
          neg[t[0]]=1   
  tokendict = we.make_token(l[1:])
  for t in tokendict:
    if(nt.has_key(t[0])):
      nt[t[0]]+=1
    else:
      nt[t[0]]=1

"""match=0
for w in neg.keys():
  if(w in pos.keys()):
    print w,neg[w]-pos[w]
print match"""

finalneg =[]
finalpos =[]
tfidf = []
tidict = {}
def caltfidf(w):
  freq=0
  if(pos.has_key(w)):
    freq+=pos[w]
  if(neg.has_key(w)):
    freq+=neg[w]
  return ((freq*1.0)/nt[w])*math.log(N/(nt[w]*1.0),2)

for w in pos:
  tfidf.append([caltfidf(w),w])
  tidict[w] = tfidf[-1][0]
for w in neg:
  if(w not in pos):
    tfidf.append([caltfidf(w),w])
    tidict[w] = tfidf[-1][0]

tfidf.sort(key=lambda x:x[0])
print tfidf
for w in pos:
  if(tidict[w]>13):
  	posfile.write(w+" "+str(pos[w])+"\n")


for w in neg:
  if(tidict[w]>13):
  	negfile.write(w+" "+str(neg[w])+"\n")






#print finalpos
#print "******************************************************************"

#print finalneg
