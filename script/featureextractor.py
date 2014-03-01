from naivefeature import *
import math
import yaml
import os

# Input only 1 OPTION, extract all features
# word: this candidate word
# Do not change vals to bools
def CandidateFeatureExtract(word, corpus = {}, confpath = ''):
  fnames = []
  fvals = []
  configs = {}
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

# Extracta all features of ONE option
def FeatureExtract(word, optnum, corpus = {}, confpath = ''):
  fnames = []
  fvals = []
  configs = {}
  if os.path.exists(confpath):
    configs = yaml.load(open(confpath))

  if 'dict' in configs:
    fnames.append('dict_'+str(optnum))
    fvals.append(DictValid(word))
  if 'wl' in configs:
    fnames.append('wl_'+str(optnum))
    fvals.append(WordLength(word))
  if 'weboccur' in configs: 
    fnames.append('occur_'+str(optnum))
    fvals.append(Occur(word))
  if 'upp' in configs:
    fnames.append('upp_'+str(optnum))
    fvals.append(UpperPunish(word))
  if 'upc' in configs:
    fnames.append('upc_'+str(optnum))
    fvals.append(ChangeTime(word))

  if 'corpus' in configs:
    fnames.append('Corpus_'+str(optnum))
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
    fnames += [s+'_'+str(optnum) for s in subs]
    fvals += values

  return fnames, fvals

# bool_dict: thresholds
def FeatureExtractAllOptions(options, corpus = {}, isBoolean=False, bool_dict = None):

  if bool_dict == None:
    bool_dict = {
      'wl': 5,
      'occur': 3,
      'upp': 0.5,
      # Default: 1
    }

  fnames = []
  fvals = []
  for optnum in range(0, len(options)):
    opt = options[optnum]
    fn, fv = FeatureExtract(opt, optnum, corpus)

    if isBoolean:
      for sub in range(0, len(fv)):
        name = fn[sub]
        val = fv[sub]
        namepref = name[:name.find('_')]

        dict_threshold = 1
        if namepref in bool_dict:
          dict_threshold = bool_dict[namepref]

        if val >= dict_threshold:
          fv[sub] = True
        else:
          fv[sub] = False

    fnames += fn
    fvals += fv


  return fnames, fvals

# import difflib
import Levenshtein, math

def FeatureExtractSuggestion(options, sugg, suggnum, corpus):
  fnames = []
  fvals = []
  suggnum = str(suggnum)
  for i in range(0, len(options)):
    opt = options[i]
    fnames.append('Dist_sug'+suggnum+'_opt'+str(i))
    dist = Levenshtein.distance(opt, sugg)  # Edit Distance
    if sugg == '':
      dist = 10
    fvals.append(dist)

    fnames.append('Ratio_sug'+suggnum+'_opt'+str(i))
    ratio = Levenshtein.ratio(opt, sugg)  # Edit Distance
    if sugg == '':
      ratio = 0.0
    fvals.append(ratio)

  fnames.append('Corpus_sug'+suggnum)
  count = 0
  if sugg in corpus:
    count = math.log(int(corpus[sugg]) + 1)
  fvals.append(count)

  fnames.append('Spell_sug'+str(suggnum))
  fvals.append(DictValid(sugg))
  fnames.append('WL_sug'+str(suggnum))
  fvals.append(WordLength(sugg))
  fnames.append('Occur_sug'+str(suggnum))
  fvals.append(Occur(sugg))
  fnames.append('UpperPunish_sug'+str(suggnum))
  fvals.append(UpperPunish(sugg))
  fnames.append('UpperChange_sug'+str(suggnum))
  fvals.append(ChangeTime(sugg))

  return fnames, fvals

def FeatureExtractAllSuggestions(options, suggestions, corpus):
  fnames = []
  fvals = []
  for suggnum in range(0, len(suggestions)):
    sugg = suggestions[suggnum]
    fn, fv = FeatureExtractSuggestion(options, sugg, suggnum, corpus)
    fnames += fn
    fvals += fv
  return fnames, fvals
