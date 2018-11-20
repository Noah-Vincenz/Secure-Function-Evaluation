
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

import json	# load
import sys	# argv

import ot	# alice, bob
import util	# ClientSocket, log, ServerSocket
import yao	# Circuit

# Alice is the circuit generator (client) __________________________________

def alice(filename):
    socket = util.ClientSocket()

    with open(filename) as json_file:
        json_circuits = json.load(json_file)

    # array of circuit strings
    circuits = []
    # array of wires strings
    for json_circuit in json_circuits['circuits']:
        # 1. create circuits
        circuit = yao.createCircuit(json_circuit)
        circuits.append(circuit)

    # 2. create wires

    # create garbled tables

    # create p-bits

    # send to bob

    # must be serialised using pickle
    socket.send(pickle.dumps(circuits))

    yao.oblivious_transfer('m0', 'm1')


# Bob is the circuit evaluator (server) ____________________________________

def bob():
  socket = util.ServerSocket()
  util.log(f'Bob: Listening ...')
  while True:
    # << removed >>
    circuits = socket.receive()
    newcircuits = pickle.loads(circuits)

# local test of circuit generation and evaluation, no transfers_____________

def local_test(filename):
  with open(filename) as json_file:
    json_circuits = json.load(json_file)

  for json_circuit in json_circuits['circuits']:
    # << removed >>

# main _____________________________________________________________________

def main():
  behaviour = sys.argv[1]
  if   behaviour == 'alice': alice(filename=sys.argv[2])
  elif behaviour == 'bob':   bob()
  elif behaviour == 'local': local_test(filename=sys.argv[2])

if __name__ == '__main__':
  main()

# __________________________________________________________________________
