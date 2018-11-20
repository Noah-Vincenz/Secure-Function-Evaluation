
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018
import util
import itertools

# << removed >>
def createCircuit(json_circuit):
    thisdict = dict()
    s = ""
    s += "======= "
    s += json_circuit["name"]
    s += " ======="
    s += "\n"
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
            thisdict[alice_gate] = permutation[i]
            s += str(permutation[i]) + " "
            i += 1
        s += "   "
        if bobGatesExist:
            listAsStr = ', '.join(str(e) for e in json_circuit["bob"])
            s += "Bob[" + listAsStr + "] = "
            for bob_gate in json_circuit["bob"]:
                thisdict[bob_gate] = permutation[i]
                s += str(permutation[i]) + " "
                i += 1
            s += "   "
        else:
            s += "Bob[] =    "
        listAsStr = ', '.join(str(e) for e in json_circuit["out"])
        s += "Outputs[" + listAsStr + "] = "
        # now alice's and bob's gates are initialised to the values in the permutation
        # we can now compute all other gates / the output gate/-s
        for gate in json_circuit["gates"]:
            truthvalue = computeTruthValue(gate["type"], gate["in"], thisdict)
            thisdict[gate["id"]] = convert_truthvalue(truthvalue)
            # now also the current gate id's value is computed
        for outputgate in json_circuit["out"]:
            s += str(thisdict[outputgate]) + " "
        s += "\n"

    return s

def convert_truthvalue(value):
    if value == True:
        return 1
    else:
        return 0

def computeTruthValue(type, arrayIn, dict):
    if type == "AND":
        return bool(dict[arrayIn[0]]) and bool(dict[arrayIn[1]])
    elif type == "OR":
        return bool(dict[arrayIn[0]]) or bool(dict[arrayIn[1]])
    elif type == "XOR":
        return bool(dict[arrayIn[0]]) != bool(dict[arrayIn[1]])
    elif type == "NOT":
        return not (bool(dict[arrayIn[0]]))
    elif type == "NOR":
        return not (bool(dict[arrayIn[0]]) or bool(dict[arrayIn[1]]))
    elif type == "NAND":
        return not (bool(dict[arrayIn[0]]) and bool(dict[arrayIn[1]]))
    elif type == "XNOR":
        return not (bool(dict[arrayIn[0]]) != bool(dict[arrayIn[1]]))

def oblivious_transfer(m0, m1):
      pg = util.PrimeGroup()
      c = pg.rand_int(pg)
      # socket.send(c)
      # socket.receive()
      x = pg.rand_int(pg)
      h_b = pg.gen_pow(pg, x)
      h_1b = pg.inv(pg, h_b)
      # send h_0 to A
      # socket.send(h_0)
      # socket.receive()
      h_1 = pg.inv(pg, h_0)
      k = pg.rand_int(pg)
      c_1 = pg.gen_pow(pg, k)
      e_0 = xor_bytes(m0, ot_hash(pg.pow(pg, h_0, k), msg_length)) #how to find msg length??
      e_1 = xor_bytes(m1, ot_hash(pg.pow(pg, h_1, k), msg_length))
      # send c1, e0, e1 to B
      # socket.send(c_1)
      # socket.receive()
      # socket.send(e_0)
      # socket.receive()
      # socket.send(e_1)
      # socket.receive()
      mb = xor_bytes(eb, ot_hash(pg.pow(pg, c_1, x), msg_length))
