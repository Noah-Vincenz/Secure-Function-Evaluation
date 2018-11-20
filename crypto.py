
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018
import json
from pprint import pprint


ENCRYPTED = True

if ENCRYPTED: #_____________________________________________________________

  # secure AES based encryption

  # << removed >>

else: # ____________________________________________________________________

  # totally insecure keyless implementation

    with open('json/f.bool.json') as f:
        data = json.load(f)

    pprint(data)

    # 'AND GATE'
    # log_and()
    # for i in range(0, 1):
    #   for j in range(0, 1):
    #       print('Alice[1]= ' + i + ' Bob[2] = ' + j + Output[3] = ' + logical_and(i,j))
  # << removed >>

# __________________________________________________________________________
