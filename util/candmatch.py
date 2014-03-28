#! /usr/bin/python

import os, sys

# e1: a variable. [cid, [wordseq]]
# match each dandidate in cands, with supvseq[index]!
# return: (T/F, [(candidate_id, cand_length_words)])
def ElemMatch(cands, supvseq, index):
  # print 'Elemmatch:',cands, index  # DEBUG
  matches = []
  for pair in cands:
    candidate_id = pair[0]
    cand_arr = pair[1]
    
    # not enough words to match
    if len(cand_arr) > len(supvseq) - index:
      # print 'Candidate too long:',cand_arr, 'for supv:',supvseq[index:index + len(cand_arr)]
      continue
    match = True
    words_tomatch = supvseq[index : index + len(cand_arr)]
    for i in range(len(words_tomatch)):
      if cand_arr[i] != words_tomatch[i]:
        match = False
        break

    if match:
      matches.append( (candidate_id, len(cand_arr)) )

  # print matches   # DEBUG
      
  if len(matches) == 0:
    return False, matches
  return True, matches
  

# return matches, matched_candidate_ids
def Match(data, supvseq):
  
  # F: longest matching up to ith element from arr1 and and jth from arr2
  arr1 = data
  arr2 = supvseq
  n1 = len(arr1)
  n2 = len(arr2)
  if n1 == 0 or n2 == 0: return 0, []

  if type(arr1[0]) != list:  # process 1-d cases
    arr1 = [ [(0, [x])] for x in data]
  
  # f = [[0] * (n2)] * (n1)  # Python array is weird....
  f = [[0] * n2 for _ in range(n1)] # This is correct way, do not give a shallow copy!!

  # record a search path to retrieve all candidate_ids.
  path = [[(-1,-1)] * n2 for _ in range(n1)]
  # retrieve what candidate to choose when optimizing f[i][j].
  cand_records = [[-1] * n2 for _ in range(n1)]

  # Init
  succ, matches = ElemMatch(arr1[0], arr2, 0)
  for pair in matches:
    candid, length = pair
    newj = 0 + length - 1
    f[0][newj] = length
    path[0][newj] = (-1, -1)  # next is root
    cand_records[0][newj] = candid
    # print 'Update',0,newj,':',candid

  # init i, 0
  for i in range(1, n1):
    
    if f[i][0] < f[i-1][0]: # SHIFT
      f[i][0] = f[i-1][0]
      p = (i-1, 0)
      # if path[i-1][0] != (-1, -1):
      #   p = path[i-1][0]
      path[i][0] = p
      # cand_records[i][0] = cand_records[i-1][0]
      cand_records[i][0] = -1

    succ, matches = ElemMatch(arr1[i], arr2, 0)
    for pair in matches:
      candid, length = pair
      newj = 0 + length - 1
      if f[i][newj] < f[i][0] + length:
        f[i][newj] = length
        path[i][newj] = (-1, -1)
        cand_records[i][newj] = candid

  # init 0, j
  for j in range(1, n2):
    # if ElemMatch(arr1[0], arr2[j]) or f[0][j-1] == 1:
    #   f[0][j] = 1
    if f[0][j] < f[0][j-1]: # SHIFT
      f[0][j] = f[0][j-1]
      p = (0, j-1)
      # if path[0][j-1] != (-1, -1):
      #   p = path[0][j-1]
      path[0][j] = p
      # cand_records[0][j] = cand_records[0][j-1]
      cand_records[0][j] = -1

    succ, matches = ElemMatch(arr1[0], arr2, j)
    for pair in matches:
      candid, length = pair
      newj = j + length - 1
      if f[0][newj] < f[0][j] + length:
        f[0][newj] = length
        path[0][newj] = (-1, -1)
        cand_records[0][newj] = candid


  # DP
  for i in range(0, n1):
    for j in range(0, n2):
      if i + 1 < n1 and j + 1 < n2:
        succ, matches = ElemMatch(arr1[i+1], arr2, j+1)
        for pair in matches:
          candid, length = pair
          newj = j + length # j+1 + length - 1
          if f[i+1][newj] < f[i][j] + length:  # refresh optimal
            f[i+1][newj] = f[i][j] + length
            path[i+1][newj] = (i, j)
            cand_records[i+1][newj] = candid

      if i + 1 < n1 and f[i+1][j] < f[i][j]: # left shift
        f[i+1][j] = f[i][j]
        # path[i+1][j] = path[i][j]
        path[i+1][j] = (i ,j)
        # cand_records[i+1][j] = cand_records[i][j]  # TODO
        cand_records[i+1][j] = -1

      if j + 1 < n2 and f[i][j+1] < f[i][j]: # right shift
        f[i][j+1] = f[i][j]
        # path[i][j+1] = path[i][j]
        path[i][j+1] = (i, j)
        # cand_records[i][j+1] = cand_records[i][j]  # TODO
        cand_records[i][j+1] = -1

  # for i in range(0, n1): 
  #   for j in range(0, n2):
  #     print '(%d,%d): %d\t' % (i,j,f[i][j]),

  matched_candids = [] # TODO not set?
  i = n1 - 1
  j = n2 - 1
  # TODO ugly..
  while (i,j) != (-1,-1): # last time: i,j != -1,-1, path == -1,-1
    if cand_records[i][j] != -1:
      matched_candids.append(cand_records[i][j])
    i, j = path[i][j]
    
  # return f[n1 - 1][n2 - 1], matched_candids
  return f[n1 - 1][n2 - 1], matched_candids, f, path, cand_records

def TestMatch(data, supvseq):
  m,can,f,path,cand_records = Match(data, supvseq)
  print 'M:',m
  print 'Can:',can[::-1]
  for i in range(len(f)):
    for j in range(len(f[i])):
      thiscanword =  ''
      for can in data[i]:
        if can[0] == cand_records[i][j]:
          thiscanword = ' '.join([str(s) for s in can[1]])

      print ' ',i,j,'\t',f[i][j],'\t','%3d,%3d'%(path[i][j][0],path[i][j][1]), '\t', cand_records[i][j], '\t%10s %10s'%(str(thiscanword), str(supvseq[j]))
  
if __name__ == "__main__": 
  if len(sys.argv) == 3:
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    arr1 = [l.strip() for l in open(f1).readlines()]
    arr2 = [l.strip() for l in open(f2).readlines()]
    m,can,f,path,cand_records =  Match(arr1, arr2)
    print m

  else:
    print 'Usage:',sys.argv[0],'<path1> <path2> (words split by \\n)'
    print 'Testing:'
    data = [
      [ 
        (123, [1,2,3]),
        (12, [1,2])
      ],
      [
        (345, [3,4,5]),
        (34, [3,4])
      ],
      [ 
        (999, [1,2,3,4,5,6,8,9,10]),
      ],
      [ 
        
        (567, [5,6,7]),
        (56, [5,6])
      ],
      [ 
        
        (98, [9,8]),
        (89, [8,9])
      ]
    ]
    supvdata = [1]
    TestMatch(data, supvdata)
    # m,can,f,path,cand_records = Match(data, supvdata)
    # print 'M:',m
    # print 'Can:',can[::-1] # reversed list
    # for i in range(len(f)):
    #   for j in range(len(f[i])):
    #     print ' ',i,j,'\t',f[i][j],'\t','%3d,%3d'%(path[i][j][0],path[i][j][1]), '\t', cand_records[i][j]
    

    # tess = [l.strip().split('\t')[5] for l in open('../data/journal-test-output3-distinct/JOURNAL_12307.cand_word').readlines() if 'T' in l.strip().split('\t')[3]]


    # # Linear match for 12307 T
    # tess = [l.strip().split('\t')[5] for l in open('../data/journal-test-output3-distinct/JOURNAL_12307.cand_word').readlines()]
    # lines = [l.strip() for l in open('../data/test-evaluation/JOURNAL_12307.seq').readlines()]
    # print 'Matching 1000 words:'
    # m,can,f,path,cand_records = Match(tess[:1000], lines[:1000])
    # print m
    # print 'Matching all words:', len(tess), len(lines)
    # m,can,f,path,cand_records = Match(tess, lines)
    # print m

    import json
    obj = json.load(open('../testgroupby-JOURNAL_14255.json'))
    docid = obj["docid"]
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

    # make sure Both data and lines are utf-8
    lines = [l.strip().decode('utf-8') for l in open('../data/test-evaluation/'+docid+'.seq').readlines()]
    print 'Matching 1000 words:'
    m,can,f,path,cand_records = Match(data[:1000], lines[:1000])
    print m
    print 'Matching all words:', len(data), len(lines)
    m,can,f,path,cand_records = Match(data, lines)
    print m


