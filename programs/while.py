import sys

n = int(sys.argv[1])

lastPrime = 2
prime = [lastPrime]

while len(prime) < n:
    lastPrime += 1
    possiblePrime = True
    i = 0
    while i < len(prime):
        if lastPrime % prime[i] == 0:
            possiblePrime = False
            break
        i += 1
    if possiblePrime:
        prime.append(lastPrime)

print(prime)
