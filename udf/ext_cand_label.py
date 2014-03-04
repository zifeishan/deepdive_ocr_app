#! /usr/bin/python

import fileinput
import json
from collections import defaultdict

# For each input tuple
for row in fileinput.input():
  obj = json.loads(row)
  cid = obj["candidate.id"]
  print json.dumps({
    "candid": cid
  })
  # Cannot manually assign ID bigserial!!?
