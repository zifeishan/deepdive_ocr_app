#! /usr/bin/python

import ddext

def init():
  ddext.input('docid', 'text')
  ddext.input('arr_candidate_id', 'bigint[]')
  ddext.input('arr_cand_word_id', 'bigint[]')
  ddext.input('arr_varid', 'bigint[]')
  ddext.input('arr_candid', 'bigint[]')
  ddext.input('arr_feature', 'text[]')
  ddext.input('gram_len', 'bigint')

  ddext.returns('docid', 'text')
  ddext.returns('cand_word_id', 'bigint')
  ddext.returns('candidate_id', 'bigint')
  ddext.returns('ngram', 'text')

def run(docid, arr_candidate_id, arr_cand_word_id, arr_varid, arr_candid, arr_feature, gram_len):

  # Store functions
  if 'AddEdge' in SD:
    AddEdge = SD['AddEdge']
  else:
    # allow multiple same edges
    def AddEdge(edges, f, t):
      if f not in edges:
        edges[f] = []
      edges[f].append(t)
    SD['AddEdge'] = AddEdge

  if 'DFS' in SD:
    DFS = SD['DFS']
  else:
    # Start with DFS(edges, id, 1)
    def DFS(docid, edges, nowid, res_array, index_cwid_sub):
      # Reaches N, finish generated a N-gram. 
      if len(res_array) == gram_len:
        feature_tmp = []
        for cwid in res_array:
          sub = index_cwid_sub[cwid]
          # Deal with range problem
          if sub >= len(arr_feature):
            plpy.info('OUT OF RANGE:' + str(arr_feature[:10]))
          else:
            feature_tmp.append(arr_feature[sub])
        feature = ' '.join([f for f in feature_tmp])
        for cwid in res_array:
          # print docid + '\t' + str(cwid) + '\t' + feature
          yield docid, cwid, arr_candidate_id[sub], feature
        return
      # Continue generating ngrams
      if nowid in edges:
        for j in edges[nowid]:
          res_array.append(j)
          # Nested yield
          for item in DFS(docid, edges, j, res_array, index_cwid_sub):
            yield item
          res_array.pop()


    SD['DFS'] = DFS

  ################## MAIN FUNCTION ####################

  # Build inverted index
  index_cwid_sub = {}
  for sub in range(len(arr_cand_word_id)):
    cwid = arr_cand_word_id[sub]
    index_cwid_sub[cwid] = sub

  if len(arr_varid) == 0:
    plpy.info('Empty data:'+str(docid))
    return

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
          plpy.info('ERROR:' + str(x) + str(y))
          continue
        AddEdge(edges, x, y)

  ###### 3. DFS output candidates
  res_array = []
  for startid in sorted(edges.keys()):
    res_array.append(startid)
    for item in DFS(docid, edges, startid, res_array, index_cwid_sub):
      yield item
    res_array.pop()

