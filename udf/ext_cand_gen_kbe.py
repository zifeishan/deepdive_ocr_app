#! /usr/bin/python
# -*- coding: utf-8 -*-

# Testing this file:
# pypy udf/ext_cand_gen_kbe.py /usr/share/dict/words 1 <data/sample-cand-gen-input.txt


import os, sys, re
# reload(sys)
# sys.setdefaultencoding('utf-8')
import codecs
# import enchant
import Levenshtein

editops_dict = {}

# Get a string of edit operations
def editops(w1, w2):

  # print >>sys.stderr, w1, w2, ':\t',

  if (w1,w2) in editops_dict:
    return editops_dict[(w1,w2)]

  ops_str = ''
  uw1 = w1.decode('utf-8')
  uw2 = w2.decode('utf-8')
  # >>>> Levenshtein.editops('Iwentu', 'I-want')
  # [('insert', 1, 1), ('replace', 2, 3), ('delete', 5, 6)]

  # apply_edit(edit_operations, source_string, destination_string)
  # In the case of editops, the sequence can be arbitrary ordered subset
  # of the edit sequence transforming source_string to destination_string.

  # Examples:
  # >>> e = editops('man', 'scotsman')
  # >>> apply_edit(e, 'man', 'scotsman')
  # 'scotsman'
  # >>> apply_edit(e[:3], 'man', 'scotsman')
  # 'scoman'
  ops = Levenshtein.editops(uw1, uw2)
  for opnum in range(len(ops)):
    (opname, sub1, sub2) = ops[opnum]
    if opname == 'delete':
      ops_str += opname[0] + uw1[sub1].encode('utf-8') + '&'
    elif opname == 'insert':
      ops_str += opname[0] + uw2[sub2].encode('utf-8') + '&'
    else:
      ops_str += opname[0] + uw1[sub1].encode('utf-8') + uw2[sub2].encode('utf-8') + '&'

    # except:
    #   print >>sys.stderr, uw1, uw2, sub1, sub2, ops

  editops_dict[(w1,w2)] = ops_str
  # print >>sys.stderr, ops_str
  return ops_str

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(BASE_DIR + '/../util/wordcorrector')
import trie

# RATIO_THRESHOLD = 0.3  # must <= this value
DISTANCE_THRESHOLD = 1
DICT_PATH = '/usr/share/dict/words'
DICT_PATH_ISDIR = False
# en_dict = enchant.Dict("en_US")

# for each word, only generate at most this many candidates 
# (0 for unrestricted)
MAXCANDNUM = 0

# Prefix of "Sg" source
SOURCE_PREFIX = ''

if len(sys.argv) >= 3:
  DICT_PATH = sys.argv[1]
  DISTANCE_THRESHOLD = int(sys.argv[2])

  if len(sys.argv) >= 4:
    MAXCANDNUM =  int(sys.argv[3])

    if len(sys.argv) >= 5:
      SOURCE_PREFIX = sys.argv[4]

# print >>sys.stderr, 'Dist: %d, maxcand: %d' % (DISTANCE_THRESHOLD, MAXCANDNUM)

# For evaluation: if DICT_PATH is directory, read "DOCID.txt" from it as kb
if os.path.isfile(DICT_PATH):
  # Init trie
  trie.init(DICT_PATH)
else:
  DICT_PATH_ISDIR = True


# Optimization: store "visited" words for candgen.
visited_results = {}


re_dash = re.compile(u'\u2013|\u2014|\u2212')
re_quote = re.compile(u'\u201d|\u201c')
re_singlequote = re.compile(u'\u2019|\u2018')

def Escape(word):
  word = re.sub(re_dash, '-', word)
  word = re.sub(re_quote, '"', word)
  word = re.sub(re_singlequote, "'", word)
  
  return word

# For each input tuple
for row in sys.stdin:
  docid, arr_varid, arr_candid, arr_word, arr_source = row.split('\t')
  print >>sys.stderr, 'Processing', docid

  # If KB path is a directory, KB=GroundTruth.
  if DICT_PATH_ISDIR:
    kbpath = DICT_PATH + '/' + docid + '.seq'
    if not os.path.isfile(kbpath):
      continue # do not generate for this document
    # lines = [l.rstrip('\n') for l in codecs.open(kbpath, 'r', 'utf-8').readlines()]
    lines = [l.rstrip('\n') for l in open(kbpath).readlines()]
    # lines = [l.rstrip('\n') for l in open(kbpath).readlines()]
    distinct_words = set(lines)
    print >>sys.stderr, 'Reading KB from', kbpath, 'MaxDist:', DISTANCE_THRESHOLD
    # trie.init()
    trie.initWithWords(distinct_words)

  arr_varid = [int(x) for x in arr_varid.rstrip().split(',')]
  arr_candid = [int(x) for x in arr_candid.rstrip().split(',')]
  arr_word = arr_word.rstrip().split('~^~')
  arr_source = arr_source.rstrip().split(',')

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

  # DEBUG
  COUNT_MINDIST_NO0 = 0
  COUNT_MINDIST_0 = 0
  num_newcands = 0
  num_newwords = 0

  # true if There are at least 1 a-z letter in s
  def IsWord(s):
    return s.lower().islower()

  def SplitPunc(s):
    n = len(s)
    puncs = ' ,.?!\':;()[]/"-='

    leftpuncs = ''
    rightpuncs = ''
    for i in range(n):
      if s[i] in puncs:
        leftpuncs += s[i]
      else:
        break

    for j in reversed(range(n)):
      if s[j] in puncs:
        rightpuncs = s[j] + rightpuncs
      else:
        break

    if i < j:
      # handle double-end spaces generated by connecting words
      return leftpuncs.strip(' '), s[i : j + 1], rightpuncs.strip(' ')
    else:  # all puncs
      return leftpuncs, '', ''




  # Returns: (words, num_edits)
  #   None: if correct or not applicatble
  #   [words]: if find a suggestion
  def SuggestCands(words):

    # "words" is a "candidate" which may consist multiple words.
    # TODO: currently we only generate ONE big thing for it...
    # e.g. "t h is" -> "this" with edit distance 2 (2 deletions)
    # This is not super systematic@

    tosearch = ' '.join(words)
    # beforeesc = tosearch
    tosearch = Escape(tosearch)  # escape rare characters!
    # if beforeesc != tosearch: print >>sys.stderr, 'ESCAPE:', beforeesc, '->',tosearch

    leftpuncs, tosearch, rightpuncs = SplitPunc(tosearch)
    if leftpuncs != '':
      leftpuncs += ' '
    if rightpuncs != '':
      rightpuncs = ' ' + rightpuncs  # for word splitting

    # Filter out punctuations / non-words
    # AD-HOC
    # if len(tosearch) <= 3 and not IsWord(tosearch):

    # if not DICT_PATH_ISDIR: # if isdir, this is evaluation, generate candidates for ALL.
    #   if not IsWord(tosearch):
    #     # if len(tosearch) > 3:
    #     #   print >>sys.stderr, 'Non-word:', tosearch
    #     return []
    if not IsWord(tosearch):
      # if len(tosearch) > 3:
      #   print >>sys.stderr, 'Non-word:', tosearch
      return []

    if tosearch not in visited_results:
      # visited_results[tosearch] = trie.search(tosearch, DISTANCE_THRESHOLD)

      # suggestions
      res = trie.searchTops(tosearch, DISTANCE_THRESHOLD, MAXCANDNUM)

      visited_results[tosearch] = res
    # return trie.search(' '.join(words), DISTANCE_THRESHOLD)
    # return visited_results[tosearch]
    # Add punctuations
    return [ 
        ( leftpuncs + x[0] + rightpuncs, x[1] )
        for x in visited_results[tosearch]]

  for varpair in data:
    varid, var = varpair
    next_candid = len(var)
    sugg_cands = {} # newcand: [(source, dist)]
    newcandids = {}
    oriwords = {}


    has_valid_candidate = False

    # TODO: now we store existing candidates in this way
    all_existing_cands = set([' '.join(cand[2]) for cand in var])

    for cand in var:
      source = cand[1]
      words = cand[2]

      ## Do not generate based on generated candidates
      # if source.endswith('Sg'):

      # can generate only based on combined candidates
      if source.endswith('Sg') or source.endswith('Seg_Presg'):
        continue

      results = SuggestCands(words)

      # print words, results
      # print 'ratio:',ratio
      if len(results) == 0: 
        continue

      # DEBUG
      # X If minimal distance == 0, we find in KB a same candidate!
      # X If some cands in "all_existing_cands", we find in KB a same candidate!
      # Therefore we do not generate ANY candidate??

      mindist = min([x[1] for x in results])
      if mindist == 0:  
        COUNT_MINDIST_0 += 1
      else:
        COUNT_MINDIST_NO0 += 1

      # if mindist != 0:
      #   print words, len(results), sorted(results, key=lambda x:x[1])[:10]
      
      # for (newcand, dist) in results:
      #   if newcand in all_existing_cands:
      #     print >>sys.stderr, '  EXISTING cand:', newcand

      ########### TODO: try to generate candidates even if exists a valid one
      # # Deal with existing candidate...
      # if any((newcand in all_existing_cands) for (newcand, dist) in results):
      #   # print 'Some existing cands:', results
      #   has_valid_candidate = True
      #   break

      # if mindist == 0:
      #   has_valid_candidate = True
      #   break


      for (newcand, dist) in results:
        # DO not generate existing candidates
        # TODO this does not count "minimal" distance..
        
        if newcand in all_existing_cands:
          # print >>sys.stderr, "Something goes wrong..", newcand
          continue

        if newcand not in sugg_cands:
          sugg_cands[newcand] = []
          newcandids[newcand] = next_candid
          oriwords[newcand] = ' '.join(words)
          next_candid += 1

        sugg_cands[newcand].append( (source, dist) )

    # Do not generate any new candidate
    if has_valid_candidate:
      continue

    # DEBUG count
    num_newcands += len(sugg_cands)

    for newcand in sugg_cands:
      # Construct a return value for generated "cand_word"
      candid = newcandids[newcand]
      pairs = sugg_cands[newcand]
      source = ''.join([x[0] for x in pairs]) + '_' + SOURCE_PREFIX + 'Sg'
      genwords = newcand.split(' ')  
      oriword = oriwords[newcand]
      # TODO now do this in a weird way...
      # Generated candidates are split into multi words by spaces

      distance = min([x[1] for x in pairs])  
      # TODO now: minimum distance

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

      # DEBUG
      num_newwords += len(genwords)
      # print >>sys.stderr, genwords

      editops_str = ''
      if distance > 0:
        editops_str = editops(oriword, newcand)
      if editops_str == '':
        editops_str = '\N'
      
      
      for wordid in range(len(genwords)):
        print '\t'.join([ str(_) for _ in [
          docid, # docid
          candidate_id + '.' + str(wordid), # cand_word_id
          candidate_id, # candidate_id
          varid, # varid
          candid, # candid
          source, # source
          wordid, # wordid
          genwords[wordid], # word
          distance, 
          # ratio,
          oriword,
          editops_str
          # '\\N'
          ]])

  # print >>sys.stderr, '0 DIST:', COUNT_MINDIST_0
  # print >>sys.stderr, 'Others:', COUNT_MINDIST_NO0
  # DEBUG
  print >>sys.stderr, '[%s] Generated %d cands (%d words) : original %d words' % (docid, num_newcands, num_newwords, len(arr_word))
    

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
/ 1. Combination
  - cross-candidate / variable 
  2. segmentation
  3. fix punctuation
'''