import sys
from BitVector import *

# Author: Tanmay Prakash
#         tprakash at purdue dot edu
# Solve x^p = y for x
# for integer values of x, y, p
# Provides greater precision than x = pow(y,1.0/p)
# Example:
# >>> x = solve_pRoot(3,64)
# >>> x
# 4L

e = 65537
#function to generate the random prime number
import random

#this is from the lecture
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

def factorize(n):                                                            #(F1)
    prime_factors = []                                                       #(F2)
    factors = [n]                                                            #(F3)
    while len(factors) != 0:                                                 #(F4)
        p = factors.pop()                                                    #(F5)
        if test_integer_for_prime(p):                                        #(F6)
            prime_factors.append(p)                                          #(F7)
            continue                                                         #(F8)
#        d = pollard_rho_simple(p)                                           #(F9)
        d = pollard_rho_strong(p)                                            #(F10)
        if d == p:                                                           #(F11)
            factors.append(d)                                                #(F12)
        else:                                                                #(F13)
            factors.append(d)                                                #(F14)
            factors.append(p//d)                                             #(F15)
    return prime_factors                                                     #(F16)

def test_integer_for_prime(p):                                               #(P1)
    probes = [2,3,5,7,11,13,17]                                              #(P2)
    for a in probes:                                                         #(P3)
        if a == p: return 1                                                  #(P4)
    if any([p % a == 0 for a in probes]): return 0                           #(P5)
    k, q = 0, p-1                                                            #(P6)
    while not q&1:                                                           #(P7)
        q >>= 1                                                              #(P8)
        k += 1                                                               #(P9)
    for a in probes:                                                         #(P10)
        a_raised_to_q = pow(a, q, p)                                         #(P11)
        if a_raised_to_q == 1 or a_raised_to_q == p-1: continue              #(P12)
        a_raised_to_jq = a_raised_to_q                                       #(P13)
        primeflag = 0                                                        #(P14)
        for j in range(k-1):                                                 #(P15)
            a_raised_to_jq = pow(a_raised_to_jq, 2, p)                       #(P16)
            if a_raised_to_jq == p-1:                                        #(P17)
                primeflag = 1                                                #(P18)
                break                                                        #(P19)
        if not primeflag: return 0                                           #(P20)
    probability_of_prime = 1 - 1.0/(4 ** len(probes))                        #(P21)
    return probability_of_prime                                              #(P22)

def pollard_rho_simple(p):                                                   #(Q1)
    probes = [2,3,5,7,11,13,17]                                              #(Q2)
    for a in probes:                                                         #(Q3)
        if p%a == 0: return a                                                #(Q4)
    d = 1                                                                    #(Q5)
    a = random.randint(2,p)                                                  #(Q6)
    random_num = []                                                          #(Q7)
    random_num.append( a )                                                   #(Q8)
    while d==1:                                                              #(Q9)
        b = random.randint(2,p)                                              #(Q10)
        for a in random_num[:]:                                              #(Q11)
            d = gcd( a-b, p )                                                #(Q12)
            if d > 1: break                                                  #(Q13)
        random_num.append(b)                                                 #(Q14)
    return d                                                                 #(Q15)

def pollard_rho_strong(p):                                                   #(R1)
    probes = [2,3,5,7,11,13,17]                                              #(R2)
    for a in probes:                                                         #(R3)
        if p%a == 0: return a                                                #(R4)
    d = 1                                                                    #(R5)
    a = random.randint(2,p)                                                  #(R6)
    c = random.randint(2,p)                                                  #(R7)
    b = a                                                                    #(R8)
    while d==1:                                                              #(R9)
        a = (a * a + c) % p                                                  #(R10)
        b = (b * b + c) % p                                                  #(R11)
        b = (b * b + c) % p                                                  #(R12)
        d = gcd( a-b, p)                                                     #(R13)
        if d > 1: break                                                      #(R14)
    return d                                                                 #(R15)

def gcd(a,b):                                                                #(S1)
    while b:                                                                 #(S2)
        a, b = b, a%b                                                        #(S3)
    return a


def generate_key(p, q):
    #e is set to be 65538
    p_file = open(p, "w")
    q_file = open(q, "w")

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
                p_file.write(str(p))
                p_file.close()
                q_file.write(str(q))
                q_file.close()
                break



def encrption(message, p, q, encryp):
    p_file = open(p, "r")
    q_file = open(q, "r")
    p_val = p_file.read()
    q_val = q_file.read()


    plain_bv = BitVector(filename = message)
    #calculate the totient based on the given p and q value
    totient = int(p_val) * int(q_val)

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

def decryption(encryp, p, q, decryp):
    p_file = open(p, "r")
    q_file = open(q, "r")
    p_val = int(p_file.read())
    q_val = int(q_file.read())

    #calculate the d value based on the bitvector mi function
    bv_t = BitVector(intVal=(p_val-1)*(q_val - 1),size=256)
    e_bv = BitVector(intVal = e)
    d_bv = e_bv.multiplicative_inverse(bv_t)
    d = d_bv.int_val()


    #calculate the totient based on the given p and q value
    totient = p_val * q_val

    #open the files
    file_in = open(encryp, "r")
    encrypted_bv = BitVector(hexstring=file_in.read())
    file_out = open(decryp, "wb")

    file_in.close()

    #iterate through the input encrpted file
    for i in range(0, len(encrypted_bv), 256):
        block = encrypted_bv[i:i+256]
        block_val = block.int_val()

        #. Use the script in the lecture notes to compute general modular exponentiation.
        M = pow(block_val, d, totient)
        decrypted_bv = BitVector(intVal=M, size=256)
        #this takes the right most 128 bits
        decrypted_bv = decrypted_bv[-128:]

        decrypted_bv.write_to_file(file_out)

    file_out.close()




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









def main():
    action = sys.argv[1]
    #check which action to do
    if(action == "-g"):
        p_file = sys.argv[2]
        q_file = sys.argv[3]
        generate_key(p_file, q_file)
    elif(action == "-e"):
        message = sys.argv[2]
        p_file = sys.argv[3]
        q_file = sys.argv[4]
        encryp = sys.argv[5]
        encrption(message, p_file, q_file, encryp)
    elif action == "-d":
        encryp = sys.argv[2]
        p_file = sys.argv[3]
        q_file = sys.argv[4]
        decryp = sys.argv[5]
        decryption(encryp, p_file, q_file, decryp)



if __name__ == '__main__':
    main()