import fileinput
import codecs
import json
import csv
import os
import sys
import json
from collections import defaultdict

# New: Add segmentation option!
# DO_SEGMENT = True
# SEGMENT_CMD = 'CLASSPATH=util/stanford-parser.jar java edu.stanford.nlp.process.PTBTokenizer -options "ptb3Escaping=false" '

# dd_output_tsv = ''
# eval_path_base = ''
# output_stat_path = ''
# this_docid = ''
# output_sequence_path = ''
sample_size = 0
docid_filter = None
# if len(sys.argv) >= 6:
if len(sys.argv) >= 5:
  dd_output_tsv = sys.argv[1]
  eval_path_base = sys.argv[2]
  output_stat_path = sys.argv[3]
  this_docid = sys.argv[4]
  # output_sequence_path = sys.argv[5]
  if len(sys.argv) >= 6:
    sample_size = int(sys.argv[5])


else:
  print 'Usage:',sys.argv[0], 'dd_output_tsv eval_path_base output_stat_path docid SAMPLESIZE'
  print 'e.g. pypy ',sys.argv[0], '/tmp/ocr-output-words-cuneiform-all.tsv lsdata/test-evaluation/ tess-eval-results/eval-JOURNAL_26741.txt JOURNAL_26741 3000'
  print 'if samplesize is 0 or not provided, do not sample.'
  sys.exit(1)
   

# GENERATE DATA with one pass
lines = [l.strip().split('\t') for l in open(dd_output_tsv).readlines()]

doc_candid_word_index = {}
doc_candidate_ids = {}
for line in lines:

  # only process one docid
  if line[0] != this_docid:
    continue

  docid, candidate_id, word = line
  if docid not in doc_candid_word_index:
    doc_candid_word_index[docid] = {}
    doc_candidate_ids[docid] = []
  data = doc_candid_word_index[docid]
  if candidate_id not in data:
    data[candidate_id] = []
    doc_candidate_ids[docid].append(candidate_id)
  data[candidate_id].append(word)

# doc_candid_word_index:  docid: { candid : [w1,w2,..] }
# doc_candidate_ids:      docid: [ candid1, candid2.. ]
eval_data = {}  # dd output data for evaluation
for docid in doc_candid_word_index:
  eval_data[docid] = []
  index = doc_candid_word_index[docid]
  cands = doc_candidate_ids[docid]
  for candid in cands:
    data = index[candid]  # [w1,w2,w3]
    cand = (candid, data)  # candidate_id, [w1,w2,w3]
    var = [cand]
    if sample_size == 0 or len(eval_data[docid]) < sample_size:
      eval_data[docid].append(var)

print 'Finished processing',len(eval_data),'documents'

fout = open(output_stat_path, 'w')
sys.path.append('util/')
import candmatch  # Use our script here


for docid in eval_data:
  data = eval_data[docid]
  evalpath = eval_path_base + '/' + docid + '.seq'
  
  if not os.path.exists(evalpath):
    print 'Error: cannot find path:',evalpath
    continue
  
  eval_sequence = [l.rstrip('\n') for l in open(evalpath).readlines()]
  if sample_size > 0:
    eval_sequence = eval_sequence[:sample_size]

  print 'Matching',docid,'...'
  matches, matched_candidate_ids, f, path, records = candmatch.Match(data, eval_sequence)

  print >>sys.stderr, 'DOCID:',docid, ' MATCHES:',matches,'/',len(eval_sequence),'(%.4f)' % (matches / float(len(eval_sequence)))

  print >>fout, '\t'.join ([str(x) for x in [docid, 
          matches, 
          len(eval_sequence), 
          matches / float(len(eval_sequence))]])


fout.close()
