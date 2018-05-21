import numpy as np
import os
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Padding
from base64 import b64decode, b64encode
import time
import random
import pickle

db = []
BLOCK_SIZE = 1
random.seed(1)
with open('keys.txt', 'rb') as file:
    sk, aes_iv = pickle.load(file)

def F(key, plaintext):
    plaintext = str(plaintext).encode()
    raw = Padding.pad(plaintext, 16)
    random.seed(1)
    cipher = AES.new(key, AES.MODE_CBC, aes_iv)
    return aes_iv + cipher.encrypt(raw)

def F_inv(key, ciphertext):
    enc = ciphertext
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return Padding.unpad(cipher.decrypt(enc[16:]), 16).decode('utf8')

def pi(key, digit):
    random.seed(key)
    s = list(range(10))
    random.shuffle(s)
    return s[digit]

def pi_inv(key, digit):
    random.seed(key)
    s = list(range(10))
    random.shuffle(s)
    return s.index(digit)

def H(text, r):
    str_to_hash = str(text)
    hasher = SHA256.new()
    hasher.update(str_to_hash.encode('utf-8'))
    hasher.update(r)
    return int(hasher.hexdigest(), 16)

def cmp(a,b):
    if a==b:
        return 0
    elif a>b:
        return 1
    else:
        return 2

def encrypt_left(sk, plaintext):
    max_input_length = 16
    digits = [int(d) for d in str(plaintext)]
    if(len(digits)>max_input_length):
        raise ValueError('Input is too large to encrypt')
    digits = [0]*(max_input_length-len(str(plaintext))) + [int(d) for d in str(plaintext)]
    u = []
    x_tilda = pi(F(sk[1], 0), digits[0])
    u.append((F(sk[0], str(0)+str(x_tilda)), x_tilda))
    for i in range(1,len(digits)):
        x_tilda = pi(F(sk[1], ''.join(map(str, digits[:i]))), digits[i])
        u.append((F(sk[0], ''.join(map(str, digits[:i]))+str(x_tilda)), x_tilda))
    return u

def encrypt_right(sk, plaintext):
    max_input_length = 16
    digits = [int(d) for d in str(plaintext)]
    if(len(digits)>max_input_length):
        raise ValueError('Input is too large to encrypt')
    digits = [0]*(max_input_length-len(str(plaintext))) + [int(d) for d in str(plaintext)]

    z = np.zeros((len(digits), 10), dtype=np.longlong)
    random.seed(1)
    r = os.urandom(16)
    for j in range(10):
        j_star = pi_inv(F(sk[1], str(0)),j)
        z[0][j] = (cmp(j_star, digits[0]) + H(F(sk[0], str(0)+str(j)), r)) % 3
    for i in range(1,z.shape[0]):
        for j in range(10):
            j_star = pi_inv(F(sk[1], ''.join(map(str, digits[:i]))),j)
            z[i][j] = (cmp(j_star, digits[i]) + H(F(sk[0], ''.join(map(str, digits[:i]))+str(j)), r)) % 3
    return (r,z)

def decrypt_right(sk, ciphertext):
    r = ciphertext[0]
    z = ciphertext[1]
    z_real = np.zeros(z.shape)
    digits = []
    for j in range(10):
        j_star = pi_inv(F(sk[1], str(0)),j)
        z_real[0][j_star] = (z[0][j]-H(F(sk[0], str(0)+str(j)), r)) % 3
    digits.append(z_real[0].tolist().index(0))
    for i in range(1,z.shape[0]):
        for j in range(10):
            j_star = pi_inv(F(sk[1], ''.join(map(str, digits[:i]))),j)
            z_real[i][j_star] = (z[i][j] - H(F(sk[0], ''.join(map(str, digits[:i]))+str(j)), r)) % 3
        digits.append(z_real[i].tolist().index(0))

    plaintext = ''.join(map(str, digits))[:-1].lstrip('0') + ''.join(map(str, digits))[-1]
    return int(plaintext)

def compare(ciphertext_left, ciphertext_right, debug=False):
    max_length_input = 16
    u = ciphertext_left
    r = ciphertext_right[0]
    z = ciphertext_right[1]
    i = 0
    l = -1
    for i in range(max_length_input):
        if ((z[i][u[i][1]] - H(u[i][0],r)%3)) % 3 != 0:
            l = i
            break

    if(l==-1):
        return 0

    else:
        res = ((z[i][u[i][1]] - H(u[i][0],r) % 3)) % 3
        if debug:
            return res
        return -1 if res == 2 else res

def test_ore(n):
    start = time.time()
    for i in range(n):
        random.seed(time.time())
        a, b = random.randint(1,1e14), random.randint(1,1e14)
        enc_a, enc_b = encrypt_left(sk, a), encrypt_right(sk, b)
        if cmp(a,b) != compare(enc_a, enc_b, True):
            print('Test Failed')
            print(a, b)
            return
    print('Test Succeeded')
    print('Time Elapsed:', time.time()-start, 'seconds')
    return

def find_place(db, ct_l):
    if len(db) == 0:
        return 0
    i = 0
    for i in range(len(db)):
        if compare(ct_l, db[i]) == -1:
            return i
    return len(db)


def insert(db, plaintext):
    ct_l = encrypt_left(sk, plaintext)
    ct_r = encrypt_right(sk, plaintext)
    db.insert(find_place(db, ct_l), ct_r)
    update(db)

def remove(db, plaintext):
    found = False
    ct_l = encrypt_left(sk, plaintext)
    for i in range(len(db)):
        if compare(ct_l, db[i]) == 0:
            found = True
            break
    if found:
        res = (db[:i] + db[i+1:]).copy()
        db[:] = res.copy()
        update(db)

def get_range(db, lower=0, upper=int(1e15)):
    enc_l_lower = encrypt_left(sk, lower)
    enc_l_upper = encrypt_left(sk, upper)
    res = []
    for i in range(len(db)):
        if compare(enc_l_lower, db[i]) <= 0 and compare(enc_l_upper, db[i]) >= 0:
            res.append(decrypt_right(sk, db[i]))

    return res

def load(db):
    if not os.path.isfile('data.txt'):
        open('data.txt', 'w+').close()
    with open('data.txt', 'rb') as file:
        try:
            db[:] = pickle.load(file)
        except EOFError:
            db[:] = []
    return

def update(db):
    open('data.txt', 'wb').close()
    with open('data.txt', 'wb') as file:
        pickle.dump(db, file)

    return

def drop(db):
    open('data.txt', 'wb').close()
    db[:] = []

def main():
    db = []
    load(db)
    query = ''
    while query != 'exit':
        query = input('> ')
        tokens = query.split()
        #print(tokens)
        if 'insert' in query:
            start = time.time()
            insert(db, int(tokens[1]))
            print('Successfully insered', int(tokens[1]))
            print(time.time()-start, 'sec.')
            continue
        if 'remove' in query:
            start = time.time()
            remove(db, int(tokens[1]))
            print('Successfully removed', int(tokens[1]))
            print(time.time()-start, 'sec.')
            continue
        if 'drop' in query:
            start = time.time()
            drop(db)
            print(time.time()-start, 'sec.')
            continue
        if 'select *' in query:
            start = time.time()
            print(get_range(db))
            print(time.time()-start, 'sec.')
            continue
        if 'select' in query and 'from' in query and 'to' in query:
            start = time.time()
            print(get_range(db, int(tokens[2]), int(tokens[4])))
            print(time.time()-start, 'sec.')
            continue
        if 'select' in query and 'from' in query:
            start = time.time()
            print(get_range(db, lower=int(tokens[2])))
            print(time.time()-start, 'sec.')
            continue
        if 'select' in query and 'to' in query:
            start = time.time()
            print(get_range(db, upper=int(tokens[2])))
            print(time.time()-start, 'sec.')
            continue
        if query != 'exit':
            print('Command not found')

if __name__ == "__main__":
    main()
