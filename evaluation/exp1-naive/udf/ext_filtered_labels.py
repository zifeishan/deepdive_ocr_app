#! /usr/bin/env python

import fileinput
import json
import csv
import os
import sys
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# For each input tuple
for row in fileinput.input():
  obj = json.loads(row)

  print json.dumps({
    "docid": obj["options.docid"],
    "wordid": obj["options.wordid"],
    "label_t": obj["labels.label_t"],
    "label_c": obj["labels.label_c"]
  })