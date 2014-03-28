#! /usr/bin/python

import fileinput
import json
import csv
import os
import sys
import json
# import yaml
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(BASE_DIR + '/../util')
import candmatch

SUPV_DIR = os.environ['SUPV_DIR']

# For each input tuple
for row in fileinput.input():
  obj = json.loads(row)

  # # DEBUG
  # # print >>sys.stderr, obj
  # fout = open('/tmp/testgroupby-' + obj['docid'] + '.json', 'w')
  # print >>fout, json.dumps(obj)
  # fout.close()

  ############### INPUT FORMAT: ###############
  # {"docid": "JOURNAL_14255",
  #  "arr_varid": [1, 2, 3, 4, 4, 5, 5, 5, 5, 5
  #  "arr_wordid": [0, 0, 0, 0,...
  #  "arr_candid": [0, 0, 0
  #  "arr_word": ["Available", "online", "at", "www.sciencedirect.corn",
  #  "arr_candidate_id": [146231, 74428, 85912, 102176, 102223, 176636,
  #  "arr_id": [98112, 98113, 98114, 98115, 98116, 98117, 98118, 98119, 98120, 98121, 98122,
  

  docid = obj["docid"]
  # arr_id = obj['arr_id']
  arr_candidate_id = obj['arr_candidate_id']
  arr_varid = obj['arr_varid']
  # arr_candid = obj['arr_candid']
  # arr_wordid = obj['arr_wordid']
  arr_word = obj['arr_word']

  if len(arr_varid) == 0:
    print >>sys.stderr, 'Empty data:',docid
    sys.exit(0)

  # Data munging
  last_varid = arr_varid[0]
  last_candidate_id = arr_candidate_id[0]
  data = []
  thisvar = []
  thiscand = []

  # # MATCHING DATA FORMAT:
  # [ 
  #   # a variable (thisvar =)
  #   [
  #     (candidate_id1, [w1 w2... wn])  # a candidate
  #     (candidate_id2, [w1 w2... wn])  # a candidate
  #   ]
  # ]

  # GENERATE DATA with one pass
  for i in range(len(arr_word)):
    varid = arr_varid[i]
    candidate_id = arr_candidate_id[i]
    word = arr_word[i]

    if candidate_id != last_candidate_id \
        or varid != last_varid:  # redundant: candidate_id is unique
      thisvar.append( (last_candidate_id, thiscand) )
      last_candidate_id = candidate_id
      thiscand = []

    if varid != last_varid:
      data.append(thisvar)
      last_varid = varid
      thisvar = []

    thiscand.append(word)

  if not os.path.exists(SUPV_DIR + '/' + docid + '.seq'):
    print >>sys.stderr, 'SUPERVISION DATA NOT EXISTS:',SUPV_DIR + '/' + docid + '.seq'
    sys.exit(0);

  supervision_sequence = [l.strip().decode('utf-8') for l in open(SUPV_DIR + '/' + docid + '.seq').readlines()]
  matches, matched_candidate_ids, f, path, records = candmatch.Match(data, supervision_sequence)

  print >>sys.stderr, 'DOCID:',docid, ' MATCHES:',matches,'/',len(supervision_sequence),'(%.4f)' % (matches / float(len(supervision_sequence)))

  for cid in matched_candidate_ids:
    print json.dumps({
      "docid": docid,
      "candidate_id": int(cid),
      "label": True
      })
