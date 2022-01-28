# Initialize a list
primes = []

for possiblePrime in range(2,70000):
    
    # Assume number is prime until shown it is not. 
    isPrime = True
    for num in range(2, possiblePrime):
        if possiblePrime % num == 0:
            isPrime = False
      
    if isPrime:
	# print("prime: " + str(possiblePrime))
        primes.append(possiblePrime)

    if len(primes) == 10000:
        print 'requestedPrime:', primes[-1]
        break
