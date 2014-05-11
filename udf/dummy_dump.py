#! /usr/bin/python

import fileinput
import json
from collections import defaultdict

fout = open('/tmp/dd_raw_json_naive.json', 'a')
# For each input tuple
for row in fileinput.input():
  print >>fout, row.strip()
  # Cannot manually assign ID bigserial!!?

fout.close()
