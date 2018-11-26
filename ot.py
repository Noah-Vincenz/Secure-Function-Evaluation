
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018
# name: Noah-Vincenz Noeh
# login: nn4718

'''
OBLIVIOUS_TRANSFERS = True

if OBLIVIOUS_TRANSFERS:
'''
import util
import sys
import pickle



def alice(m_0, m_1, socket):

    msg_length = 64
    print('m0', m_0)
    G, c, m_0_msg_length, m_1_msg_length = compute_c(m_0, m_1)
    socket.send(pickle.dumps(G))
    socket.receive()
    socket.send(pickle.dumps(c))
    h_0 = pickle.loads(socket.receive())
    c_1, e_0, e_1 = compute_c1_e0_e1(G, c, msg_length, m_0_msg_length, m_1_msg_length, h_0)
    socket.send(pickle.dumps([c_1, e_0, e_1]))
    socket.receive()
    pass

def compute_c(m_0, m_1):
    """
    Alice computes c from a G
    returns G, c, message length of m_0 and m_1
    """
    G = util.PrimeGroup()
    print(G)
    g = G.generator
    m_0_msg_length = pickle.dumps(m_0)
    m_1_msg_length = pickle.dumps(m_1)
    return G, G.rand_int(), m_0_msg_length, m_1_msg_length

def compute_c1_e0_e1(G, c, msg_length, m_0_msg_length, m_1_msg_length, h_0):
    """
    Alice computes c_1, e_0 and e_1
    returns c_1, e_0 and e_1 for Bob, which he will be able to use to finally decrypt the message
    """
    h_1 = G.mul(c, G.inv(h_0))
    k = G.rand_int()
    c_1 = G.gen_pow(k)
    H_0 = util.ot_hash(G.pow(h_0, k), msg_length)
    H_1 = util.ot_hash(G.pow(h_1, k),  msg_length)
    e_0 = util.xor_bytes(m_0_msg_length, H_0)
    e_1 = util.xor_bytes(m_1_msg_length, H_1)
    return c_1, e_0, e_1

def bob(b, socket):

    msg_length = 64
    G = pickle.loads(socket.receive())
    socket.send("")
    c = pickle.loads(socket.receive())
    x, h_0 = compute_h0(G, c, b)
    socket.send(pickle.dumps(h_0))
    c_1, e_0, e_1 = pickle.loads(socket.receive())
    socket.send("")
    plaintext = decrypt_msg(G, x, b, msg_length, c_1, e_0, e_1)
    return plaintext

def compute_h0(G, c, b):
    """
    Bob computes h_0
    returns h_0 only
    """
    x = G.rand_int()
    h_b = G.gen_pow(x)
    h_1_minus_b = G.mul(c, G.inv(h_b))
    h_0 = h_b
    if(b == 0):
        return x, h_b
    else:
        return x, h_1_minus_b

def decrypt_msg(G, x, b, msg_length, c_1, e_0, e_1):
    """
    Bob finally decrypts the message to get the plaintext
    returns the plaintext message
    """
    hash = util.ot_hash(G.pow(c_1, x), msg_length)
    print('message decrypted')
    if(b == 0):
        print(util.xor_bytes(e_0, hash))
        return util.xor_bytes(e_0, hash)
    else:
        print(util.xor_bytes(e_1, hash))
        return util.xor_bytes(e_1, hash)

def main():
    behaviour = sys.argv[1]
    c_socket = util.ClientSocket()
    s_socket = util.ServerSocket()
    if   behaviour == 'alice': alice("a", "b", c_socket)
    elif behaviour == 'bob':   bob(1, s_socket)
    #elif behaviour == 'local': local_test(filename=sys.argv[2])

if __name__ == '__main__':
    main()
