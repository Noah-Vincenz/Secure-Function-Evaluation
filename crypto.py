
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018
# name: Noah-Vincenz Noeh
# login: nn4718

from cryptography.fernet import Fernet
import pickle

ENCRYPTED = True

if ENCRYPTED:

  # secure AES based encryption

    def encrypt(keyA, keyB, keyC, xor):
        f1 = Fernet(keyA)

        if keyB != "NOT":

            f2 = Fernet(keyB)
            secret = pickle.dumps((keyC, xor))
            first_ciphertext = f1.encrypt(secret)
            return f2.encrypt(first_ciphertext)

        else:

            secret = pickle.dumps((keyC, xor))
            return f1.encrypt(secret)

    def decrypt(keyA, keyB, ciphertext):

        if keyB != "NOT":

           f1 = Fernet(keyB)
           f2 = Fernet(keyA)
           new_ciphertext = f1.decrypt(ciphertext)
           x = f2.decrypt(new_ciphertext)
           (keyC, xor) = pickle.loads(x)

        else:

           f = Fernet(keyA)
           (keyC, xor) = pickle.loads(f.decrypt(ciphertext))

        xor = int(xor)
        return (keyC, xor)
