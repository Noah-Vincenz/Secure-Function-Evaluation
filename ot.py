
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

OBLIVIOUS_TRANSFERS = True

if OBLIVIOUS_TRANSFERS: # __________________________________________________

  # bellare-micali OT with naor and pinkas optimisations, see smart p423

  # << removed >>
  pg = PrimeGroup()

  c = pg.rand_int(pg)
  # send c to B
  x = pg.rand_int(pg)
  h_b = pg.gen_pow(pg, x)
  h_1b = pg.inv(pg, h_b)
  # send h_0 to A
  h_1 = pg.inv(pg, h_0)
  k = pg.rand_int(pg)
  c_1 = pg.gen_pow(pg, k)
  e_0 = xor_bytes(m0, ot_hash(pg.pow(pg, h_0, k), msg_length))
  e_1 = xor_bytes(m1, ot_hash(pg.pow(pg, h_1, k), msg_length))
  # send c1, e0, e1 to B 
  mb = xor_bytes(eb, ot_hash(pg.pow(pg, c_1, x), msg_length))


else: # ____________________________________________________________________

  # non oblivious transfers, not even a secure channel is used, for testing

  # << removed >>

# __________________________________________________________________________
