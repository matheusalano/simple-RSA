import sys
from random import getrandbits, randrange
from math import gcd

def generateRandomPrime():
    primeCandidate = getrandbits(1024)
    
    while pow(2, primeCandidate-1, primeCandidate) != 1:
        primeCandidate = getrandbits(1024)
    
    return primeCandidate

def getPublicKey(eulerN):
    e = randrange(1, eulerN)
    g = gcd(e, eulerN)
    while g != 1:
        e = randrange(1, eulerN)
        g = gcd(e, eulerN)
    return e

def generateKeys():
    prime1 = generateRandomPrime()
    prime2 = generateRandomPrime()

    N = prime1 * prime2
    eulerN = (prime1 - 1) * (prime2 - 1)

    e = getPublicKey(eulerN)
    d = extendedEuclidean(e, eulerN)[1]
    d = d+eulerN if d < 0 else d

    return (e, N), (d, prime1, prime2)

def extendedEuclidean(x, y):
    if y == 0:
        return (x, 1, 0)
    else:
        d1, a1, b1 = extendedEuclidean(y, x % y)
        d = d1
        a = b1
        b = a1 - (x // y) * b1
        return (d, a, b)
    
def encrypt(M, PK):
    C = pow(M, PK[0], PK[1])
    return C

def decrypt(C, SK):
    M = pow(C, SK[0], SK[1] * SK[2])
    return M

if __name__ == "__main__":
    sys.setrecursionlimit(1000000)

    PK, SK = generateKeys()
    print('Public Key', PK)
    print('Secret Key', SK)

    M = input('Enter your message:')
    C = encrypt(int(M), PK)

    print('Encrypted message: ', C)

    DM = decrypt(C, SK)

    print('Decrypted message: ', DM)

    # Caso precise aceitar string -> https://gist.github.com/JekaDeka/c9b0f5da16625e3c7bd1033356354579