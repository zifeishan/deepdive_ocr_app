#! /usr/bin/env python

import fileinput
import json
import csv
import os
import sys
import json
import yaml
from collections import defaultdict

flibpath = os.environ['FEATURE_LIB_PATH']
sys.path.append(flibpath)
import alignment

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Input only 1 OPTION, extract all features
# word: this candidate word
def CandidateFeatureExtract(word, corpus = {}, confpath = ''):
  fnames = []
  fvals = []
  configs = {}
  if confpath == '' and 'FEATURE_CONF_PATH' in os.environ:
    confpath = os.environ['FEATURE_CONF_PATH']

  if os.path.exists(confpath):
    configs = yaml.load(open(confpath))

  if 'dict' in configs:
    fnames.append('dict')
    fvals.append(DictValid(word))
  if 'wl' in configs:
    fnames.append('wl')
    fvals.append(WordLength(word))
  if 'weboccur' in configs: 
    fnames.append('occur')
    fvals.append(Occur(word))
  if 'upp' in configs:
    fnames.append('upp')
    fvals.append(UpperPunish(word))
  if 'upc' in configs:
    fnames.append('upc')
    fvals.append(ChangeTime(word))

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
    fnames += [s for s in subs]
    fvals += values

  return fnames, fvals

# For each input tuple
for row in fileinput.input():
  obj = json.loads(row)
  word = obj["candidate.word"]
  fnames, fvals = CandidateFeatureExtract(word)
  for i in range(0, len(fname)):
    if fvals[i] == False:
      continue
    print json.dumps({
      "candidateid": obj["candidate.id"]
      "fname": fnames[i]
      "fval": fvals[i]
    })
