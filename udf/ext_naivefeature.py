#! /usr/bin/python

import fileinput
import json
import csv
import os
import sys
import json
# import yaml
from collections import defaultdict

flibpath = ''
if 'FEATURE_LIB_PATH' in os.environ:
  flibpath = os.environ['FEATURE_LIB_PATH']
  sys.path.append(flibpath)
else:
  sys.path.append('script')

print >>sys.stderr, 'FEATURE_LIB_PATH:', flibpath

# from alignment import *
from naivefeature import *

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Input only 1 OPTION, extract all features
# word: this candidate word
def CandidateFeatureExtract(word, source, corpus = {}, confpath = ''):
  fnames = []
  fvals = []
  configs = {}

  # if confpath == '' and 'FEATURE_CONF_PATH' in os.environ:
  #   confpath = os.environ['FEATURE_CONF_PATH']

  # if os.path.exists(confpath):
  #   configs = yaml.load(open(confpath))

  configs = {
    'char1gram': '-,.?![]"\'{}',
    'char2gram': ['fi','fl','rn', 'rm','nn'],
    'dict': True,
    'upp': True,
    'upc': True,
    'wl': True,
    'notascii': True,
    'bool_dict': {'wl': 5, 'occur': 3, 'upp': 0.5}}


  if 'dict' in configs:
    fnames.append('dict')
    fvals.append(DictValid(word))
  if 'wl' in configs:
    fnames.append('wl_'+source)
    fvals.append(WordLength(word))
  if 'weboccur' in configs: 
    fnames.append('occur')
    fvals.append(Occur(word))
  if 'upp' in configs:
    fnames.append('upp_'+source)
    fvals.append(UpperPunish(word))
  if 'upc' in configs:
    fnames.append('upc_'+source)
    fvals.append(ChangeTime(word))
  if 'notascii' in configs:
    fnames.append('notascii_'+source)
    fvals.append(not IsASCII(word))


  if 'corpus' in configs:
    fnames.append('Corpus')
    count = 0
    if word in corpus:
      count = math.log(corpus[word] + 1)
    fvals.append(count)

  # subs, values = CntAllSubstr(word)
  if 'char1gram' in configs or 'char2gram' in configs:
    c1g = ''
    c2g = []
    if 'char1gram' in configs: c1g = configs['char1gram']
    if 'char2gram' in configs: c2g = configs['char2gram']
    subs, values = CntReducedSubStr(word, c1g, c2g)
    fnames += [s + '_' + source for s in subs]
    fvals += values

  # To boolean: default dict
  bool_dict = {
    'wl': 5,
    'occur': 3,
    'upp': 0.5,
    # Default: 1
  }
  if 'bool_dict' in configs:
    bool_dict = configs['bool_dict']
    for i in range(0, len(fnames)):
      # name = fnames[i]
      name = fnames[i].split('_')[0]

      threshold = 1
      if name in bool_dict:
        threshold = bool_dict[name] 
      # print fnames[i], fvals[i], threshold
      if fvals[i] < threshold:
        fvals[i] = False
      else:
        fvals[i] = True

  return fnames, fvals

# For each input tuple
for row in fileinput.input():
  docid, cand_word_id, word, source = row.split('\t')
  fnames, fvals = CandidateFeatureExtract(word, source)
  for i in range(0, len(fnames)):
    if fvals[i] == False:
      continue
    # Weird: no strip there is '\n'???
    print '\t'.join([str(_).strip() for _ in [docid, cand_word_id, fnames[i], fvals[i]]])

    # print json.dumps({
    #   # "candidateid": obj["candidate.id"],
    #   "cand_word_id": obj["id"],
    #   "fname": fnames[i],
    #   "fval": fvals[i]
    # })
