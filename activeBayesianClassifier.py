def bayesianClassifier(pos,neg,tokens):
	prob = [1.0,1.0]
	posl = len(pos)
	negl = len(neg)
	V = len(pos)+len(neg)
	checkp = False
	checkn = False
	for w in tokens :
		if(w in pos or w in neg):
			if w in neg:
				checkn = True
				prob[0] = prob[0]*(2.0/(negl+V))
				prob[1] = prob[1]*(1.0/(posl+V))
			else:
				checkp = True
				prob[0] = prob[0]*(1.0/(negl+V))
				prob[1] = prob[1]*(2.0/(posl+V))
	if(checkp==1 or checkn==1):
		prob.append(1)
	else:
		prob.append(0)
	return prob

def bayesianClassifier2(pos,neg,posl,negl,tokens):
  prob = [1.0,1.0]
  V = len(pos)+len(neg)
  checkp = False
  checkn = False
  if(len(tokens)==0):
    return -1
  for w in tokens :
    if(w in neg):
      checkn = True
      prob[0] = prob[0]*(((neg[w]+1)*1.0)/(negl+V))
    else:
      prob[0] = prob[0]*(1.0/(negl+V))
    if(w in pos):
      checkp = True
      prob[1] = prob[1]*(((pos[w]+1)*1.0)/(posl+V))
    else:
      prob[1] = prob[1]*(1.0/(posl+V))
  if(checkp==1 or checkn==1):
    prob.append(1)
  else:
    prob.append(0)
  if(prob[0]>prob[1]):
    return 0
  elif(prob[1]>prob[0]):
    return 1
  else:
    return -1
