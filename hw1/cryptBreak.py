#Arguments:
# ciphertextFile: String containing file name of the ciphertext (e.g. encrypted.txt )
# key_bv: 16-bit BitVector of the key used to try to decrypt the ciphertext.
#Function Description:
# Attempts to decrypt ciphertext contained in ciphertextFile using key_bv and returns
# the original plaintext as a string
from BitVector import *

BLOCKSIZE = 16
numbytes = BLOCKSIZE // 8

PassPhrase = "Hopes and dreams of a million years"


def cryptBreak(ciphertextFile,key_bv):
    # Reduce the passphrase to a bit array of size BLOCKSIZE:
    bv_iv = BitVector(bitlist=[0] * BLOCKSIZE)  # (F)
    a = numbytes
    for i in range(0, len(PassPhrase) // numbytes):  # (G)
        textstr = PassPhrase[i * numbytes:(i + 1) * numbytes]  # (H)
        bv_iv ^= BitVector(textstring=textstr)  # (I)

    # Create a bitvector from the ciphertext hex string:
    FILEIN = open(ciphertextFile)  # (J)
    encrypted_bv = BitVector(hexstring=FILEIN.read())  # (K)

    # Create a bitvector for storing the decrypted plaintext bit array:
    msg_decrypted_bv = BitVector(size=0)  # (T)

    # Carry out differential XORing of bit blocks and decryption:
    previous_decrypted_block = bv_iv  # (U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):  # (V)
        bv = encrypted_bv[i * BLOCKSIZE:(i + 1) * BLOCKSIZE]  # (W)
        temp = bv.deep_copy()  # (X)
        bv ^= previous_decrypted_block  # (Y)
        previous_decrypted_block = temp  # (Z)
        bv ^= key_bv  # (a)
        msg_decrypted_bv += bv  # (b)

    # Extract plaintext from the decrypted bitvector:
    outputtext = msg_decrypted_bv.get_text_from_bitvector()  # (c)

    return outputtext


if __name__ == '__main__':
    for i in range(2**16):
        someRandomInteger = 9999  # Arbitrary integer for creating a BitVector
        key_bv = BitVector(intVal=i, size=16)
        decryptedMessage = cryptBreak('encrypted.txt', key_bv)
        print(decryptedMessage)
        print("\n")
        if 'Mark Twain' in decryptedMessage:
            print('Encryption Broken!')
            print(i)
            break
        else:
            print('Not decrypted yet')