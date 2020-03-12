import hashlib


def hash():
    file = open("message.txt", "r")
    test = open("test.txt", "w")
    text = file.read()
    hasher = hashlib.sha512()
    hasher.update(text.encode('utf-8'))

    res = hasher.hexdigest()

    test.write(res)

    file.close()
    test.close()



if __name__ == '__main__':
    hash()