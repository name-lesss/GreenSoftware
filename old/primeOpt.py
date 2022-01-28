#1000ste priem getal
lastPrime = 2
priem = [lastPrime]
requestedPrime = 10000

while len(priem) < requestedPrime:
    lastPrime+=1
    possiblePriem = True
    for i in range(len(priem)) :
        if lastPrime%priem[i]==0 :
            possiblePriem = False;
    if possiblePriem==True :
        priem.append(lastPrime)

print 'requestedPrime:', priem[requestedPrime-1]
