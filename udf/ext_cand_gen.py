#! /usr/bin/python

# Testing this file:
# pypy udf/ext_cand_gen.py 3 /tmp/tmp_cand_gen_ <data/sample-cand-gen-input.txt

import os, sys
import codecs
import enchant
import Levenshtein

DICT_THRESHOLD = 3
TMP_PREFIX = '/tmp/tmp_cand_gen_'
RATIO_THRESHOLD = 0.3  # must <= this value
# DISTANCE_THRESHOLD = 5

en_dict = enchant.Dict("en_US")

if len(sys.argv) >= 3:
  DICT_THRESHOLD = int(sys.argv[1])
  TMP_PREFIX = sys.argv[2]

# For each input tuple
for row in sys.stdin:
  docid, arr_varid, arr_candid, arr_word, arr_source = row.split('\t')
  print >>sys.stderr, 'Processing', docid

  arr_varid = [int(x) for x in arr_varid.rstrip().split(',')]
  arr_candid = [int(x) for x in arr_candid.rstrip().split(',')]
  arr_word = arr_word.rstrip().split('~^~')
  arr_source = arr_source.rstrip().split(',')

  # count word frequency
  freqmap = {}
  for w in arr_word:
    if w not in freqmap:
      freqmap[w] = 0
    freqmap[w] += 1

  # print freqmap

  # build dict file
  dict_words = [w for w in freqmap if freqmap[w] >= DICT_THRESHOLD]

  # print 'Constructing dict..'
  # corpus_dict = enchant.Dict()
  corpus_dict = enchant.request_pwl_dict(TMP_PREFIX + docid)
  for w in dict_words: 
    corpus_dict.add_to_pwl(w)

  # print corpus_dict
  # print 'Done constructing dict.'

  # Data munging
  last_varid = arr_varid[0]
  last_candid = arr_candid[0]
  last_source = arr_source[0]
  data = []
  thisvar = []
  thiscand = []

  # GENERATE DATA with one pass
  for i in range(len(arr_word)):
    varid = arr_varid[i]
    candid = arr_candid[i]
    word = arr_word[i]
    source = arr_source[i]

    if candid != last_candid \
        or varid != last_varid:  # redundant: candid is unique
      thisvar.append( (last_candid, last_source, thiscand) )
      last_candid = candid
      last_source = source
      thiscand = []

    if varid != last_varid:
      data.append((last_varid, thisvar))
      last_varid = varid
      thisvar = []

    thiscand.append(word)

  # print data[:10]

  # data: [vars]
  # var: (varid,[cands])
  # cand: (candid, source, [words])

  # Possible methods: (1) go from each candidate (2) go from all candidates
  # currently taking 1.

  # Returns: (words, num_edits)
  #   None: if correct or not applicatble
  #   [words]: if find a suggestion
  def SuggestCand(words):
    ret = []
    total_edits = 0
    total_err_ratio = 0.0
    iscorrect = True
    for word in words:
      if en_dict.check(word) or corpus_dict.check(word):
        ret.append(word)
      else:
        iscorrect = False
        sugg_list = corpus_dict.suggest(word)
        if len(sugg_list) == 0: 
          return None, 0, 0.
        # sorted_suggs = sorted(sugg_list, key=lambda sw: Levenshtein.ratio(word, sw), reverse=True)
        best_sugg = max(sugg_list, key=lambda sw: Levenshtein.ratio(word, sw))
        for w in best_sugg.split(' '):
          ret.append(w)
        total_edits += Levenshtein.distance(word, best_sugg)
        total_err_ratio += 1.0 - Levenshtein.ratio(word, best_sugg)
    if iscorrect: 
      return None, 0, 0.

    if total_err_ratio > RATIO_THRESHOLD: return None, 0, 0.

    return ret, total_edits, total_err_ratio


  for varpair in data:
    newcands = []
    varid, var = varpair
    next_candid = len(var)
    distinct_sugg_cands = set()
    for cand in var:
      source = cand[1]
      words = cand[2]
      sugg_words, distance, ratio = SuggestCand(words)
      # print 'ratio:',ratio

      if sugg_words != None:
        sw_str = ' '.join(sugg_words)
        if sw_str in distinct_sugg_cands: continue  # do not add it

        distinct_sugg_cands.add(sw_str)
        # candid, source, words
        newcand = (next_candid, source+'Sg', sugg_words, distance, words)
        next_candid += 1
        newcands.append(newcand)

    for newcand in newcands:
      # Construct a return value for generated "cand_word"
      candid = newcand[0]
      source = newcand[1]
      words = newcand[2]
      distance = newcand[3]
      original_word = newcand[4]
      candidate_id = docid + '@' + str(varid) + '_' + str(candid)
      
      # Returns: create table generated_cand_word(
      #     cand_word_id  TEXT,
      #     candidate_id  TEXT,
      #     docid         TEXT,
      #     varid         INT,      -- start from 1
      #     candid        INT,      -- start from 0, according to source
      #     source        TEXT,     -- 1-1 mapping to source
      #     wordid        INT,      -- start from 0
      #     word          TEXT
      #     )
      
      for wordid in range(len(words)):
        print '\t'.join([ str(_) for _ in [
          candidate_id + '.' + str(wordid), # cand_word_id
          candidate_id, # candidate_id
          docid, # docid
          varid, # varid
          candid, # candid
          source, # source
          wordid, # wordid
          words[wordid], # word
          distance, 
          # ratio,
          # ' '.join(original_word)  # can open when debugging
          ]])

  # for i in range(len(arr_word)):
  #   word = arr_word[i]
  #   varid = arr_varid[i]
  #   # print word
  #   if not en_dict.check(word):  # not valid word in dict
  #     # print 'invalid!'
  #     # get closest cand in dict
  #     sugg_list = corpus_dict.suggest(word)
  #     if len(sugg_list) > 0:
  #       sorted_suggs = sorted(sugg_list, key=lambda sw: Levenshtein.ratio(word, sw), reverse=True)
  #       # sorted_suggs = sorted(sugg_list, key=lambda sw: Levenshtein.distance(word, sw))

  #       # print 'Invalid:',word
  #       # print 'Suggestions:', sorted_suggs
        
'''
TODO:
1. Combination
2. segmentation
3. fix punctuation
'''