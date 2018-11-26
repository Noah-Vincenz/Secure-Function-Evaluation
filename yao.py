# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018
# name: Noah-Vincenz Noeh
# login: nn4718

import itertools
import random
import crypto
import pickle
from cryptography.fernet import Fernet


### MILLIONAIRES PROBLEM MISSING
### EVALUATION AT a implies b CIRCUIT FAILS DUE TO DECRYPTION ERROR WITH FERNETTOKENEXCEPTION


# 1 for encryption of value 0, one for encryption of value 1
def create2RandomKeys():
    """
    Create and return two random keys using th Fernet library:
    1) for the 0 value
    2) for the 1 value
    """
    return (Fernet.generate_key().decode("utf-8"), Fernet.generate_key().decode("utf-8"))

def write_circuit(json_circuit):
    """
    Write the circuit to the output file and create all the wires in the circuit for Bob and return:
    1) s: string to write to the output file - truth table
    2) wires_dict: a dictionary that maps wire id's to it's pbit and keys and
    3) pbits_dict: a dictionary that maps output wire id's to their corresponding pbit.
    """
    wires_dict = {}
    pbits_dict = {}
    gate_dict = {}
    s = ""
    noOfAliceGates = len(json_circuit["alice"])
    bobGatesExist = True
    if "bob" not in json_circuit:
        bobGatesExist = False
        noOfBobGates = 0
    else:
        noOfBobGates = len(json_circuit["bob"])
    noOfAllGates = noOfAliceGates + noOfBobGates
    # ie [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    permutations = list(itertools.product([0, 1], repeat=noOfAllGates))
    # iterate through every permutation to compute truth table for every combination
    for permutation in permutations:
        i = 0
        listAsStr = ', '.join(str(e) for e in json_circuit["alice"])
        s += "Alice[" + listAsStr + "] = "
        for alice_gate in json_circuit["alice"]:
            #gate_dict[alice_gate] = permutation[i]
            s += str(permutation[i]) + " "
            p_bit = random.randint(0,1)
            (key_zero, key_one) = create2RandomKeys()
            print(alice_gate)
            wires_dict[alice_gate] = {}
            wires_dict[alice_gate]["pbit"] = p_bit
            wires_dict[alice_gate]["keys"] = [key_zero, key_one]
            gate_dict[alice_gate] = permutation[i]
            i += 1
        s += "   "
        if bobGatesExist:
            listAsStr = ', '.join(str(e) for e in json_circuit["bob"])
            s += "Bob[" + listAsStr + "] = "
            for bob_gate in json_circuit["bob"]:
                #gate_dict[bob_gate] = permutation[i]
                s += str(permutation[i]) + " "
                p_bit = random.randint(0,1)
                (key_zero, key_one) = create2RandomKeys()
                wires_dict[bob_gate] = {}
                wires_dict[bob_gate]["pbit"] = p_bit
                wires_dict[bob_gate]["keys"] = [key_zero, key_one]
                gate_dict[bob_gate] = permutation[i]
                i += 1
            s += "   "
        else:
            s += "Bob[] =    "

        listAsStr = ', '.join(str(e) for e in json_circuit["out"])
        s += "Outputs[" + listAsStr + "] = "
        # now alice's and bob's gates are initialised to the values in the permutation
        # we can now compute all other gates / the output gate/-s
        for gate in json_circuit["gates"]:

            p_bit = random.randint(0,1)
            (key_zero, key_one) = create2RandomKeys()
            print(gate)
            wires_dict[gate["id"]] = {}
            wires_dict[gate["id"]]["pbit"] = p_bit
            wires_dict[gate["id"]]["keys"] = [key_zero, key_one]
            this_gate = find_gate(gate["id"], json_circuit)
            if len(this_gate["in"]) == 1:
                truthvalue = logical_operator("NOT", [gate_dict[this_gate["in"][0]]])
            else:
                truthvalue = logical_operator(this_gate["type"], [gate_dict[this_gate["in"][0]], gate_dict[this_gate["in"][1]]])
            gate_dict[gate["id"]] = truthvalue

            # now also the current gate id's value is computed
        for outputgate in json_circuit["out"]:
            gate = find_gate(outputgate, json_circuit)
            if len(gate["in"]) == 1:

                truthvalue = logical_operator("NOT", [gate_dict[gate["in"][0]]])

            else:

                truthvalue = logical_operator(gate["type"], [gate_dict[gate["in"][0]], gate_dict[gate["in"][1]]])

            s += str(truthvalue) + " "
            gate_dict[outputgate] = truthvalue
            pbits_dict[outputgate] = wires_dict[outputgate]["pbit"]
        s += "\n"

    return (s, wires_dict, pbits_dict)

def find_gate(gate_id, json_circuit):
    for gate in json_circuit["gates"]:
        if gate["id"] == gate_id:
            return gate

def garble_table(json_circuit, wires_dict):
    """
    Construct the garbled tables and return a dictionary that maps gate ids to the corresponding list of encrypted output keys
    """
    garbled_tables_dict = {}
    pbits_in = []

    for gate in json_circuit["gates"]:
        # garbled table - list of encrypted output keys for each gate for every 0/1 state
        output_keys = []

        # 1: get the input wires and output wire
        input_wires = gate["in"]
        output_wire = gate["id"]

        # 2: get the pbits of the input wires and of output wire
        #pbits_in = []
        for input_wire in input_wires:
            pbits_in.append(wires_dict[input_wire]["pbit"])
        pbit_out = wires_dict[output_wire]["pbit"]

        if gate["type"] == "NOT":

            for i in range(0, 2):
                xor1 = logical_operator("XOR", [i, pbits_in[0]])
                result = logical_operator(gate["type"], [xor1])
                xor_result = logical_operator("XOR", [result, pbit_out])
                keyA = wires_dict[input_wires[0]]["keys"][xor1] # since xor1 is either 0 or 1 depending on p_bit -> key is randomly picked
                keyC = wires_dict[output_wire]["keys"][result]
                enc = crypto.encrypt(keyA, "NOT", keyC, xor_result)
                output_keys.append(enc)

        else:
            for i in range(0, 2):
                output_keys.append([])
                for j in range(0, 2):
                    xor1 = logical_operator("XOR", [i, pbits_in[0]])
                    xor2 = logical_operator("XOR", [j, pbits_in[1]])
                    result = logical_operator(gate["type"], [xor1, xor2])
                    xor_result = logical_operator("XOR", [result, pbit_out])
                    keyA = wires_dict[input_wires[0]]["keys"][xor1] # since xor1 is either 0 or 1 depending on p_bit -> key is randomly picked
                    keyB = wires_dict[input_wires[1]]["keys"][xor2] # since xor2 is either 0 or 1 depending on p_bit -> key is randomly picked
                    keyC = wires_dict[output_wire]["keys"][result]
                    if json_circuit["name"] == "A implies B":
                        print("ENCRYPTING WITH KEYS FOR i,j = ", i, ',', j)
                        print(keyA, keyB)
                    enc = crypto.encrypt(keyA, keyB, keyC, xor_result)
                    output_keys[-1].append(enc)

        garbled_tables_dict[output_wire] = output_keys

    return garbled_tables_dict


def logical_operator(operator, inputs):
    if operator == "AND":
        i1, i2 = inputs
        return max(0, i1 + i2 - 1)

    elif operator == "OR":
        i1, i2 = inputs
        return min(1, i1 + i2)

    elif operator == "XOR":
        i1, i2 = inputs
        return 1 - (i1 == i2)

    elif operator == "NOT":
        return 1 - inputs[0]

    elif operator == "NOR":
        i1, i2 = inputs
        return 1 - min(1, i1 + i2)

    elif operator == "NAND":
        i1, i2 = inputs
        return 1 - max(0, i1 + i2 - 1)

    elif operator == "XNOR":
        i1, i2 = inputs
        return int(i1 == i2)

def evaluate (json_circuit, garbled_tables_dict, input_key_xor_dict, pbits_dict):
    """
    Evaluates the garbled circuit and returns the output values of the gates
    """
    for gate in json_circuit["gates"]:
        output_values = []
        id = gate["id"]
        input_wires = gate["in"]
        keyA, xor1 = input_key_xor_dict[input_wires[0]]
        if gate["type"] != "NOT":
            keyB, xor2 =  input_key_xor_dict[input_wires[1]]
            if json_circuit["name"] == "A implies B":
                print("DECRYPTING WITH KEYS")
                print(keyA, keyB)
            garbled_entry = garbled_tables_dict[id][xor1][xor2]
            input_key_xor_dict[id] = crypto.decrypt(keyA, keyB, garbled_entry)
        else:
            garbled_entry = garbled_tables_dict[id][xor1]
            input_key_xor_dict[id] = crypto.decrypt(keyA, "NOT", garbled_entry)

    for output_wire in json_circuit["out"]:
        (key, xored_input) = input_key_xor_dict[output_wire]
        output_values.append(logical_operator("XOR", [xored_input, pbits_dict[output_wire]]))

    return output_values
