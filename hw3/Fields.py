import sys

input = sys.argv[1]




#In order to determine Zn is a field, we have to check whether the n is a prime or not
#If it is prime, according to the lecture slides, it is a field, otherwise it is a ring
#The reason behind it is because when n is prime, every number in the set will satisify a * b mod n = 0, then a or b
#must be 0

def check_prime(num):
    if(num == 0 or num == 1):
        return False
    #check every number in the field to see whehter n can be divisible by the num
    for n in range(0,num-1):
        if num % n == 0:
            return False


    return True



if check_prime(input):
    print("Field")
else:
    print("Ring")