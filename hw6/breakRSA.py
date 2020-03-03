import sys
from BitVector import *

import random
e = 3

#this is from the lecture
import numpy as np
import sys

def solve_pRoot(p,y):
    p = int(p)
    y = int(y)
    # Initial guess for xk
    try:
        xk = int(pow(y,1.0/p))
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y
        a = 0
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1
            a += 1
        # log xk = log2 y / p
        # log xk = (a + log2 y0) / p
        xk = int(pow(2.0, ( a + np.log2(float(y0)) )/ p ))

    # Solve for x using Newton's Method
    err_k = int(pow(xk,p))-y
    while (abs(err_k) > 1):
        gk = p*int(pow(xk,p-1))
        err_k = int(pow(xk,p))-y
        xk = int(-err_k/gk) + xk
    return xk





############################  class PrimeGenerator  ##############################
class PrimeGenerator( object ):                                              #(A1)

    def __init__( self, **kwargs ):                                          #(A2)
        bits = debug = None                                                  #(A3)
        if 'bits' in kwargs  :     bits = kwargs.pop('bits')                 #(A4)
        if 'debug' in kwargs :     debug = kwargs.pop('debug')               #(A5)
        self.bits            =     bits                                      #(A6)
        self.debug           =     debug                                     #(A7)
        self._largest        =     (1 << bits) - 1                           #(A8)

    def set_initial_candidate(self):                                         #(B1)
        candidate = random.getrandbits( self.bits )                          #(B2)
        if candidate & 1 == 0: candidate += 1                                #(B3)
        candidate |= (1 << self.bits-1)                                      #(B4)
        candidate |= (2 << self.bits-3)                                      #(B5)
        self.candidate = candidate                                           #(B6)

    def set_probes(self):                                                    #(C1)
        self.probes = [2,3,5,7,11,13,17]                                     #(C2)

    # This is the same primality testing function as shown earlier
    # in Section 11.5.6 of Lecture 11:
    def test_candidate_for_prime(self):                                      #(D1)
        'returns the probability if candidate is prime with high probability'
        p = self.candidate                                                   #(D2)
        if p == 1: return 0                                                  #(D3)
        if p in self.probes:                                                 #(D4)
            self.probability_of_prime = 1                                    #(D5)
            return 1                                                         #(D6)
        if any([p % a == 0 for a in self.probes]): return 0                  #(D7)
        k, q = 0, self.candidate-1                                           #(D8)
        while not q&1:                                                       #(D9)
            q >>= 1                                                          #(D10)
            k += 1                                                           #(D11)
        if self.debug: print("q = %d  k = %d" % (q,k))                       #(D12)
        for a in self.probes:                                                #(D13)
            a_raised_to_q = pow(a, q, p)                                     #(D14)
            if a_raised_to_q == 1 or a_raised_to_q == p-1: continue          #(D15)
            a_raised_to_jq = a_raised_to_q                                   #(D16)
            primeflag = 0                                                    #(D17)
            for j in range(k-1):                                             #(D18)
                a_raised_to_jq = pow(a_raised_to_jq, 2, p)                   #(D19)
                if a_raised_to_jq == p-1:                                    #(D20)
                    primeflag = 1                                            #(D21)
                    break                                                    #(D22)
            if not primeflag: return 0                                       #(D23)
        self.probability_of_prime = 1 - 1.0/(4 ** len(self.probes))          #(D24)
        return self.probability_of_prime                                     #(D25)

    def findPrime(self):                                                     #(E1)
        self.set_initial_candidate()                                         #(E2)
        if self.debug:  print("    candidate is: %d" % self.candidate)       #(E3)
        self.set_probes()                                                    #(E4)
        if self.debug:  print("    The probes are: %s" % str(self.probes))   #(E5)
        max_reached = 0                                                      #(E6)
        while 1:                                                             #(E7)
            if self.test_candidate_for_prime():                              #(E8)
                if self.debug:                                               #(E9)
                    print("Prime number: %d with probability %f\n" %
                          (self.candidate, self.probability_of_prime) )      #(E10)
                break                                                        #(E11)
            else:                                                            #(E12)
                if max_reached:                                              #(E13)
                    self.candidate -= 2                                      #(E14)
                elif self.candidate >= self._largest - 2:                    #(E15)
                    max_reached = 1                                          #(E16)
                    self.candidate -= 2                                      #(E17)
                else:                                                        #(E18)
                    self.candidate += 2                                      #(E19)
                if self.debug:                                               #(E20)
                    print("    candidate is: %d" % self.candidate)           #(E21)
        return self.candidate                                                #(E22)

def gcd(a,b):                                                                #(S1)
    while b:                                                                 #(S2)
        a, b = b, a%b                                                        #(S3)
    return a

def generate_key():
    #the size is required to be 128 bits
    prime_g = PrimeGenerator(bits = 128)
    # two left-most bits of both p and q must be set

    while(1):

        # two left-most bits of both p and q must be set
        p = prime_g.findPrime()
        q = prime_g.findPrime()
        # p and q must not be equal to each other
        if p != q:
            # (p-1) co-prime to (q-1)
            if gcd((p - 1), e) == 1 and gcd((q - 1), e) == 1:
                return p*q


def encryption():
    pass








#use crt to find the modular exponentiation
def crt(C, d, p, q):
    #calculate Vp and Vq based lecture 34 page
    Vp = pow(C, (d % (p-1)), p)
    Vq = pow(C, (d % (q-1)), q)

    bv_p = BitVector(intVal=p)
    bv_q = BitVector(intVal=q)
    invp = bv_q.multiplicative_inverse(bv_p)
    p_inv = invp.int_val()
    invq = bv_p.multiplicative_inverse(bv_q)
    q_inv = invq.int_val()

    Xp = q * (q_inv % p)
    Xq = p * (p_inv % q)


    Cd_mod_n = (Vp * Xp + Vq * Xq) % (p * q)

    return Cd_mod_n



def encrption(message, totient, encryp):
    plain_bv = BitVector(filename = message)
    #calculate the totient based on the given p and q value

    file_out = open(encryp, "w")


    #Your data block from the text will be of 128-bits,  prepend itwith 128 zeroes on the left to make it a 256-bit block
    #if the overall plaintext length is not a multiple of 128 bits
    while plain_bv.more_to_read:
        bv = plain_bv.read_bits_from_file(128)
        if bv.length() < 128:
            bv.pad_from_right(128 - bv.length())
        #pad the left with 128 zeros
        bv.pad_from_left(128)


        #rsa encrption  Med = Med = m mod n, n is the totient
        encp_val = pow(bv.int_val(), e, totient)
        bv_e = BitVector(intVal=encp_val, size=256)

        #write the bitvector to the file
        file_out.write(bv_e.get_hex_string_from_bitvector())

    file_out.close()



def main():
    pattern = sys.argv[1]
    n_list = list()
    for i in range(3):
        n_list.append(generate_key())

    d_list = list()
    for n in n_list:
        e_bv = BitVector(intVal=e)
        n_bv = BitVector(intVal=n)
        d = e_bv.multiplicative_inverse(n_bv)
        d = d.int_val()
        d_list.append(d)

    if pattern == "-e":
        message = sys.argv[2]
        enc1 = sys.argv[3]
        enc2 = sys.argv[4]
        enc3 = sys.argv[5]
        n_file = sys.argv[6]
    elif pattern == "-c":
        enc1 = sys.argv[2]
        enc2 = sys.argv[3]
        enc3 = sys.argv[4]
        n_file = sys.argv[5]
        craked = sys.argv[6]
    else:
        raise ValueError("The input from the system is wrong")