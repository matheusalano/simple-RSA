import sys
from random import getrandbits, randrange
from math import gcd
import binascii

def stringToInt(text, N):
    hex_data = binascii.hexlify(text.encode())
    plain_text = int(hex_data, 16)

    if plain_text > N:
        raise Exception('plain text too large for key')

    return plain_text

def intToString(decrypted_text, N):
    hex_data = hex(decrypted_text)[2:]

    return binascii.unhexlify(hex_data).decode()

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
    intM = stringToInt(M, PK[1])
    C = pow(intM, PK[0], PK[1])
    return C

def decrypt(C, SK):
    #Verificar se hex(C)[2:] for > 512 pegar os 512 e decriptar até terminar
    M = pow(C, SK[0], SK[1] * SK[2])
    return intToString(M, SK[1] * SK[2])

if __name__ == "__main__":
    sys.setrecursionlimit(1000000)

    print('Options: \n1 - Generate secret and public key\n2 - Encrypt a message\n3 - Decrypt a message\n4 - Stop')
    PK = None
    SK = None
    while True:
        option = input('Enter the option: ')

        if option == '1':
            PK, SK = generateKeys()
            print(f'Public Key: {PK[0]}, {PK[1]}')
            print(f'Secret Key: {SK[0]}, {SK[1]}, {SK[2]}')
        elif option == '2':
            PK = input('Enter Public Key separated by comma: ')
            PK = PK.split(', ')
            PK = (int(PK[0]), int(PK[1]))

            M = input('Enter your message: ')
            C = encrypt(M, PK)

            print('Encrypted message: ', C)
        elif option == '3':
            SK = input('Enter Secret Key separated by comma: ')
            SK = SK.split(', ')
            SK = (int(SK[0]), int(SK[1]), int(SK[2]))
            
            C = input('Enter the encrypted message: ')
            DM = decrypt(int(C), SK)

            print('Decrypted message: ', DM)
        elif option == '4':
            exit(0)
        else:
            print('Wrong option.')