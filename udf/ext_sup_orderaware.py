#! /usr/bin/python

import fileinput
import json
import csv
import os
import sys
import json
# import yaml
from collections import defaultdict
import codecs

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(BASE_DIR + '/../util')
import candmatch

SUPV_DIR = os.environ['SUPV_DIR']

IS_EVALUATION = False
bestpick_dir = ''

min_distance = 0
max_distance = 0

if len(sys.argv) >= 3:
    bestpick_dir = sys.argv[1]
    SUPV_DIR = sys.argv[2]
    print >>sys.stderr, "NOTE: you should already EMPTY the directory", SUPV_DIR
    print >>sys.stderr, "Using EVAL_DIR as SUPV_DIR:", SUPV_DIR
    print >>sys.stderr, "Storing bestpick results into:", bestpick_dir
    IS_EVALUATION = True

    if len(sys.argv) == 5:
      print >>sys.stderr, 'Distance range:', sys.argv[3:]
      min_distance = int(sys.argv[3])
      max_distance = int(sys.argv[4])

# For each input tuple
for row in sys.stdin:
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

  # # DEBUG
  # arr_candidate_id = arr_candidate_id[:100]
  # arr_varid = arr_varid[:100]
  # arr_word = arr_word[:100]

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

  # TODO didn't add the last element?

  if not os.path.exists(SUPV_DIR + '/' + docid + '.seq'):
    print >>sys.stderr, 'SUPERVISION DATA NOT EXISTS:',SUPV_DIR + '/' + docid + '.seq'
    sys.exit(1);

  supervision_sequence = [l.strip().decode('utf-8') for l in open(SUPV_DIR + '/' + docid + '.seq').readlines()]

  # print 'IS_EVALUATION:',IS_EVALUATION
  if not IS_EVALUATION:
    matches, matched_candidate_ids, f, path, records = candmatch.Match(data, supervision_sequence)

    print >>sys.stderr, 'DOCID:',docid, ' MATCHES:',matches,'/',len(supervision_sequence),'(%.4f)' % (matches / float(len(supervision_sequence)))

  else:  # is evaluation: generate optimal for 0--X
    for dist in range(min_distance, max_distance + 1):

      # print >>sys.stderr, 'Evaluating distance:', dist
    

      matches, matched_candidate_ids, f, path, records = candmatch.Match(data, supervision_sequence, dist)

      print >>sys.stderr, 'D=%d: DOCID:' % dist, docid, ' MATCHES:',matches,'/',len(supervision_sequence),'(%.4f)' % (matches / float(len(supervision_sequence)))

      # store bestpick results      
      statdir = bestpick_dir
      if not os.path.exists(statdir):
        os.makedirs(statdir)
      fout = open(statdir + docid + '.stat.' + str(dist), 'w')
      print >>fout, '\t'.join([str(s) for s in [
        docid, matches, len(supervision_sequence), 
        '(%.4f)' % (matches / float(len(supervision_sequence)))
        ]])
      fout.close()

      fout = codecs.open(statdir + docid + '.seq.' + str(dist), 'w', 'utf-8')
      matched_candidate_ids_index = set(matched_candidate_ids)
      for var in data:
        for cand in var:
          if cand[0] in matched_candidate_ids_index:
            for w in cand[1]:
              print >>fout, w
      fout.close()


  for cid in matched_candidate_ids:
    print json.dumps({
      "docid": docid,
      "candidate_id": cid,
      "label": True
      })
