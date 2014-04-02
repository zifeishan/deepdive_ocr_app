import fileinput
import codecs
import json
import csv
import os
import sys
import json
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(BASE_DIR + '/../')
import candmatch

# obj = json.load(open('../testgroupby/testgroupby-JOURNAL_12307.json'))
obj = json.load(open('../testgroupby/testgroupby-JOURNAL_6056.json'))

SUPV_DIR = '../data/test-evaluation/'

# For each input tuple
docid = obj["docid"]
print docid
arr_candidate_id = obj['arr_candidate_id']
arr_varid = obj['arr_varid']
arr_word = obj['arr_word']

# Data munging
last_varid = arr_varid[0]
last_candidate_id = arr_candidate_id[0]
data = []
thisvar = []
thiscand = []

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
  print 'SUPERVISION DATA NOT EXISTS:',SUPV_DIR + '/' + docid + '.seq'
  sys.exit(0);

supervision_sequence = [l.strip().decode('utf-8') for l in open(SUPV_DIR + '/' + docid + '.seq').readlines()]
# matches, matched_candidate_ids, f, path, records = candmatch.Match(data[:100], supervision_sequence[:100])

print 'Dumping upper bound choices:'
fout = codecs.open('test-all.tmp', 'w', 'utf-8')
for var in data:
  for cand in var:
    for w in cand[1]:
      print >>fout, w
fout.close()

print 'Test Match:'
candmatch.TestMatch(data[:1000], supervision_sequence[:1000])

print 'Real matching...'
matches, matched_candidate_ids, f, path, records = candmatch.Match(data, supervision_sequence)

print >>sys.stderr, 'DOCID:',docid, ' MATCHES:',matches,'/',len(supervision_sequence),'(%.4f)' % (matches / float(len(supervision_sequence)))


print 'Dumping optimal choices:'
fout = codecs.open('test-optimal.tmp', 'w', 'utf-8')
matched_candidate_ids_index = set(matched_candidate_ids)
for var in data:
  for cand in var:
    if cand[0] in matched_candidate_ids_index:
      for w in cand[1]:
        print >>fout, w
fout.close()

# TESS ONLY
print 'TESS ONLY:'
tdata = [[v[-1]] for v in data]
matches, matched_candidate_ids, f, path, records = candmatch.Match(tdata, supervision_sequence)

print >>sys.stderr, 'DOCID:',docid, ' MATCHES:',matches,'/',len(supervision_sequence),'(%.4f)' % (matches / float(len(supervision_sequence)))

fout = codecs.open('test-tesseract-diff.tmp', 'w', 'utf-8')
for var in tdata:
  for w in var[0][1]:
    print >>fout, w
fout.close()

