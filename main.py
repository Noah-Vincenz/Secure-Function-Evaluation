
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018
# name: Noah-Vincenz Noeh
# login: nn4718

import json
import sys
import ot
import util
import yao
import pickle
import crypto

# Alice is the circuit generator (client) __________________________________

def alice(filename):
    socket = util.ClientSocket()

    with open(filename) as json_file:
        file_name = filename
        json_circuits = json.load(json_file)

    # output file to which the results are written to
    output_file = open("output_tests", "a")

    # array of wires strings
    for json_circuit in json_circuits['circuits']:
        #if json_circuit["name"] == "NOT using NAND":
            output_file.write("======= " + json_circuit["name"] + " =======\n")

            # create wires, create p-bits
            #wires_dict, pbits_dict = yao.initiate_wires(json_circuit)
            s, wires_dict, pbits_dict = yao.write_circuit(json_circuit)

            if "bob" not in json_circuit:

                output_file.write(s)

            else:

                socket.send(pickle.dumps(json_circuit))
                socket.receive()
                output_file.write(s)

                socket.send(pickle.dumps(wires_dict))
                socket.receive()
                socket.send(pickle.dumps(pbits_dict))
                socket.receive()

                # create garbled tables
                garbled_tables_dict = yao.garble_table(json_circuit, wires_dict)

                socket.send(pickle.dumps(garbled_tables_dict))
                socket.receive()

                wires_alice = json_circuit["alice"]
                no_wires_alice = len(wires_alice)
                wires_bob = json_circuit["bob"]
                no_wires_bob = len(wires_bob)

                input_alice = {}

                for i in range(2**no_wires_alice):

                    # take bits from after the first two bits and pad binary number with zeros on the left
                    binary_a = bin(i)[2:].zfill(no_wires_alice)

                    for wire_a in range(no_wires_alice):
                        wire_id = wires_alice[wire_a]
                        key = wires_dict[wire_id]["keys"][int(binary_a[wire_a])]
                        pbit = wires_dict[wire_id]["pbit"]
                        xor = yao.logical_operator("XOR", [pbit, int(binary_a[wire_a])])
                        input_alice[wire_id] = [key, xor]

                    socket.send(pickle.dumps(input_alice))
                    socket.receive()

                    for j in range(2**no_wires_bob):

                        # take bits from after the first two bits and pad binary number with zeros on the left
                        binary_b = bin(j)[2:].zfill(no_wires_bob)

                        for wire_b in range(no_wires_bob):

                            wire_id = wires_bob[wire_b]
                            keyA, keyB = wires_dict[wire_id]["keys"]
                            pbit = wires_dict[wire_id]["pbit"]
                            m_0 = keyA + "," + str(yao.logical_operator("XOR", [pbit, 0]))
                            m_1 = keyB + "," + str(yao.logical_operator("XOR", [pbit, 1]))
                            print('Alices message m0: ', m_0)
                            print('Alices message m1: ', m_1)
                            ot.alice(m_0, m_1, socket)

                        socket.send("")
                        outputs = pickle.loads(socket.receive())

    output_file.close()


# Bob is the circuit evaluator (server) ____________________________________

def bob():
  socket = util.ServerSocket()
  util.log(f'Bob: Listening ...')

  while True:
    json_circuit = pickle.loads(socket.receive())
    socket.send("Bob received json_circuit.")
    wires_dict = pickle.loads(socket.receive())
    socket.send("Bob received wires_dict.")
    pbits_dict = pickle.loads(socket.receive())
    socket.send("Bob received pbits_dict.")
    garbled_tables_dict = pickle.loads(socket.receive())
    socket.send("Bob received garbled_tables_dict.")

    wires_alice = json_circuit["alice"]
    no_wires_alice = len(wires_alice)
    wires_bob = json_circuit["bob"]
    no_wires_bob = len(wires_bob)
    input_bob = [j for j in range(2**no_wires_bob)]

    for i in range(2**no_wires_alice):

        input_alice = pickle.loads(socket.receive())
        socket.send("")

        input_key_xor_dict = input_alice

        for j in range(2**no_wires_bob):
            binary = bin(j)[2:].zfill(no_wires_bob)
            for wire in range(no_wires_bob):
                input_bit = int(binary[wire])
                wire_id = wires_bob[wire]
                decrypted_msg = pickle.loads(ot.bob(input_bit, socket))
                print('Bobs Decrypted Message: ', decrypted_msg)
                key, xor = decrypted_msg.split(",")
                input_key_xor_dict[wire_id] = [key, int(xor)]

            socket.receive()

            print(json_circuit, "\n")
            print(garbled_tables_dict, "\n")
            print(input_key_xor_dict, "\n")
            print(pbits_dict, "\n")

            outputs = yao.evaluate(json_circuit, garbled_tables_dict, input_key_xor_dict, pbits_dict)
            socket.send(pickle.dumps(outputs))
            print("Finished")

'''
# local test of circuit generation and evaluation, no transfers_____________

def local_test(filename):
  with open(filename) as json_file:
    json_circuits = json.load(json_file)

  for json_circuit in json_circuits['circuits']:
    print('')
'''
# main _____________________________________________________________________

def main():
  behaviour = sys.argv[1]
  if   behaviour == 'alice': alice(filename=sys.argv[2])
  elif behaviour == 'bob':   bob()
  # elif behaviour == 'local': local_test(filename=sys.argv[2])

if __name__ == '__main__':
  main()

# __________________________________________________________________________
