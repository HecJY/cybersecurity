#!/usr/bin/env python3

import sys
from BitVector import *
AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption
invSubBytesTable = []                                               # for decryption

def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

def encryption(round_keys, bitvec):

    #init state array
    statearray = [[0 for x in range(4)] for x in range(4)]




    if bitvec.size > 0:
        if len(bitvec) != 128:
                # fiil the array when the bit count is not 128

            bitvec.pad_from_right(128 - len(bitvec))

        #xor with bit vector each time
    bitvec = bitvec ^ round_keys[0]
    for i in range(4):
        for j in range(4):
            statearray[j][i] = bitvec[32 * i + 8 * j:32 * i + 8 * (j + 1)]


    for i in range(1, 15):
            #sub bytes
        for x in range(0, 4):
            for y in range(0, 4):
                    statearray[x][y] = BitVector(intVal=subBytesTable[int(statearray[x][y])], size=8)
        #shift row
        statearray = shift_rows(statearray, False)

        #mixing col
        if i != 14:
            statearray = mix_col(statearray)
        #generate round keys
        round_key = round_keys[i]
        state_array = BitVector(size=128)
        for i in range(4):
            for j in range(4):
                state_array[32 * i + 8 * j:32 * i + 8 * (j + 1)] = statearray[j][i]

        temp = state_array ^ round_key
        for i in range(4):
            for j in range(4):
                statearray[j][i] = temp[32 * i + 8 * j:32 * i + 8 * (j + 1)]

    temp1 = BitVector(size=128)
    for i in range(4):
        for j in range(4):
            temp1[32 * i + 8 * j:32 * i + 8 * (j + 1)] = statearray[j][i]

    return temp1

def mix_col(statearray):
    new_state = statearray.copy()
    #create the constant for the statearray
    hex_2 = BitVector(intVal=2, size=8)
    hex_3 = BitVector(intVal=3, size=8)

    final_state = list()
    #iterate through each row
    pos = 0
    for x in range(0,4):
        first_row = hex_2.gf_multiply_modular(statearray[0][x], AES_modulus, 8) ^ hex_3.gf_multiply_modular(statearray[1][x], AES_modulus, 8) ^ statearray[2][x] ^ statearray[3][x]
        second_row = hex_2.gf_multiply_modular(statearray[1][x], AES_modulus, 8) ^ hex_3.gf_multiply_modular(statearray[2][x], AES_modulus, 8) ^ statearray[3][x] ^ statearray[0][x]
        third_row = hex_2.gf_multiply_modular(statearray[2][x], AES_modulus, 8) ^ hex_3.gf_multiply_modular(statearray[3][x], AES_modulus, 8) ^ statearray[0][x] ^ statearray[1][x]
        forth_row = hex_2.gf_multiply_modular(statearray[3][x], AES_modulus, 8) ^ hex_3.gf_multiply_modular(statearray[0][x], AES_modulus, 8) ^ statearray[1][x] ^ statearray[2][x]

        new_state[0][x] = first_row
        new_state[1][x] = second_row
        new_state[2][x] = third_row
        new_state[3][x] = forth_row

    return new_state

def shift_rows(state_array, inv):
    row = [[0, 1, 2, 3],
           [1, 2, 3, 0],
           [2, 3, 0, 1],
           [3, 0, 1, 2]]

    inv_row = [[0, 1, 2, 3],
               [3, 0, 1, 2],
               [2, 3, 0, 1],
               [1, 2, 3, 0]]
    #for a state array

    if(inv):
        for x in range(0, 4):
            for y in range(0, 4):
                col = inv_row[x][y]
                inv_row[x][y] = state_array[x][col]

        return inv_row
    else:
        for x in range(0, 4):
            for y in range(0, 4):
                col = row[x][y]
                row[x][y] = state_array[x][col]
        return row




def gen_key(keyfile):
    key_words = []
    key_bv = get_key_from_user(keyfile)
    key_words = gen_key_schedule_256(key_bv)
    key_schedule = []
    num_rounds = 14
    #print("\nEach 32-bit word of the key schedule is shown as a sequence of 4 one-byte integers:")
    for word_index, word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i * 8:i * 8 + 8].intValue())
        if word_index % 4 == 0: print("\n")
        #print("word %d:  %s" % (word_index, str(keyword_in_ints)))
        key_schedule.append(keyword_in_ints)
    round_keys = [None for i in range(num_rounds + 1)]
    for i in range(num_rounds + 1):
        round_keys[i] = (key_words[i * 4] + key_words[i * 4 + 1] + key_words[i * 4 + 2] +
                         key_words[i * 4 + 3])

    return round_keys

def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal =
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8]
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words



def get_key_from_user(keyfile):
    keysize = 256
    file = open(keyfile, "r")
    key = file.readline()
    key = key.strip()
    key += '0' * (keysize//8 - len(key)) if len(key) < keysize//8 else key[:keysize//8]
    key_bv = BitVector( textstring = key )
    return key_bv


def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable



def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant





#Arguments:
# iv: 128-bit initialization vector
# image_file: input .ppm image file name
# out_file: encrypted .ppm image file name
# key_file: String of file name containing encryption key (in ASCII)
#Function Descrption:
# Encrypts image_file using CTR mode AES and writes said file to out_file. No
#required return value.
def ctr_aes_image(iv, image_file= 'image.ppm',out_file= 'enc_image.ppm', key_file= 'key.txt'):
    #open the image file, read the file header, then put it in the out put encrypted file (hw2)
    file = open(image_file, "rb")
    file_out = open(out_file, "wb")

    image_info = file.readlines()
    #write header to the file
    file_out.writelines(image_info[0:3])
    image_bv = BitVector(filename=image_file)
    #skip the headers, because the header length is 14 for ppm
    image_bv.read_bits_from_file(14 * 8)

    #generate the round keys first
    genTables()
    round_keys = gen_key(key_file)

    while (image_bv.more_to_read):
        bitvec = image_bv.read_bits_from_file(128)
        if bitvec.size > 0:
            if len(bitvec) != 128:
                # fiil the array when the bit count is not 128
                bitvec.pad_from_right(128 - len(bitvec))

        #encryp the iv first
        iv_encrypted = encryption(round_keys, iv)

        cyphertext = iv_encrypted ^ bitvec


        #write cypertext to the file, update the iv
        cyphertext.write_to_file(file_out)
        #update iv
        temp = iv.int_val() + 1
        iv = BitVector(intVal=temp, size = 128)


    file_out.close()


if __name__ == '__main__':
    iv = BitVector(textstring='computersecurity')  # iv will be 128 bits
    ctr_aes_image(iv,'image.ppm', 'enc_image_temp.ppm', 'key.txt')
