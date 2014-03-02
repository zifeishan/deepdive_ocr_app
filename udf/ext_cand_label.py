#! /usr/bin/python

import fileinput
import json
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# For each input tuple
for row in fileinput.input():
  obj = json.loads(row)
  cid = obj["candidate.id"]
  for i in range(0, len(fnames)):
    if fvals[i] == False:
      continue
    print json.dumps({
      "id": cid
    })
