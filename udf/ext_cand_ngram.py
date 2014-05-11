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

NGRAM = 2

id_fgram_dict = {}

if len(sys.argv) >= 2:
  NGRAM = int(sys.argv[1])  # input number of grams

# allow multiple same edges
def AddEdge(edges, f, t):
  if f not in edges:
    edges[f] = []
  edges[f].append(t)

# Start with DFS(edges, id, 1)
def DFS(docid, edges, nowid, res_array, arr_candidate_id, arr_feature, index_cwid_sub):

  # Reaches N, finish generated a N-gram. 
  if len(res_array) == NGRAM:
    # print res_array   ## contains all cwids in the ngram

    # print json.dumps({
    #   "arr_cand_word_id": res_array
    #   })
    feature_tmp = []
    # candidate_ids = set()
    for cwid in res_array:
      sub = index_cwid_sub[cwid]
      # candidate_ids.add(arr_candidate_id[sub])

      # Deal with range problem
      if sub >= len(arr_feature):
        print >>sys.stderr, 'OUT OF RANGE:', sub, len(arr_feature)
        print >>sys.stderr, '  ', arr_feature[:10]
      else:
        feature_tmp.append(arr_feature[sub])

    # feature = ' '.join(str(f) for f in feature_tmp)  # word gram, pos gram, etc
    ### UTF-8 problem if "str"
    feature = ' '.join([f for f in feature_tmp])  # word gram, pos gram, etc

    # Table format:
    # #   candidate_id BIGSERIAL, ### WRONG LOGIC
    #   cand_word_id BIGSERIAL, ### WRONG LOGIC
    #   feature_gram TEXT
    for cwid in res_array:
      print docid + '\t' + str(cwid) + '\t' + feature
      # print json.dumps({
      #   "cand_word_id": cwid,
      #   "feature_gram": feature
      #   })

    return   # Finished. Recurse.

  if nowid not in edges: return

  for j in edges[nowid]:
    res_array.append(j)
    DFS(edges, j, res_array, arr_candidate_id, arr_feature, index_cwid_sub)
    res_array.pop()




# For each input tuple
# for row in fileinput.input():  # This cannot take arguments
for row in sys.stdin:
# # DEBUG
# for row in open('test/test-ext_cand_ngram.json').readlines():

  # obj = json.loads(row)
  parts = row.rstrip('\n').split('\t')
  if len(parts) != 6: 
    print >>sys.stderr, 'ERROR: Failed to parse row:', row
    continue


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
  #  "arr_cand_word_id": [146231, 74428, 85912, 102176, 102223, 176636,
  #  "arr_id": [98112, 98113, 98114, 98115, 98116, 98117, 98118, 98119, 98120, 98121, 98122,
  

  docid = parts[0]
  # arr_id = obj['arr_id']
  arr_candidate_id = [int(x) for x in parts[1].split(',')]
  arr_cand_word_id = [int(x) for x in parts[2].split(',')]
  arr_varid = [int(x) for x in parts[3].split(',')]
  arr_candid = [int(x) for x in parts[4].split(',')]
  arr_feature = parts[5].split('~^~')
  # TODO support WORD / POS

  # Build inverted index
  index_cwid_sub = {}
  for sub in range(len(arr_cand_word_id)):
    cwid = arr_cand_word_id[sub]
    index_cwid_sub[cwid] = sub

  if len(arr_varid) == 0:
    print >>sys.stderr, 'Empty data:',docid
    sys.exit(0)

  ######### 1. build directed graph
  last_varid = arr_varid[0]
  last_candid = arr_candid[0]
  last_cand_word_id = -1
  
  edges = {}  # cand_word_id1 : [cand_word_id2]
  startw = {} # var : [a list of start words]
  endw = {}   # var : [a list of end words]

  for i in range(len(arr_candid)):

    cand_word_id = arr_cand_word_id[i]
    varid = arr_varid[i]
    candid = arr_candid[i]

    # same candidate
    if last_varid == varid and last_candid == candid:  
      if last_cand_word_id != -1:
        AddEdge(edges, last_cand_word_id, cand_word_id)
      else:  # FIRST CANDIDATE
        AddEdge(startw, last_varid, cand_word_id)

    # change candidate, may or may not change variable
    if last_varid != varid or last_candid != candid:
      AddEdge(startw, varid, cand_word_id)  # this start
      AddEdge(endw, last_varid, last_cand_word_id) # last end

    # Update "last" elements
    last_varid = varid
    last_candid = candid
    last_cand_word_id = cand_word_id

  # Add last element
  AddEdge(endw, last_varid, last_cand_word_id)

  ####### 2. build edges across variable
  for varid in sorted(endw.keys()):
    arr1 = endw[varid]
    if varid + 1 not in startw: continue
    arr2 = startw[varid + 1]
    for x in arr1:
      for y in arr2:
        if x == y:
          print >>sys.stderr, 'ERROR:', x, y
          continue
        AddEdge(edges, x, y)

  ###### 3. DFS output candidates
  
  res_array = []
  for startid in sorted(edges.keys()):
    res_array.append(startid)
    DFS(docid, edges, startid, res_array, arr_candidate_id, arr_feature, index_cwid_sub)
    res_array.pop()

