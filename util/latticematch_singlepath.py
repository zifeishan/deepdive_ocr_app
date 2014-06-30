#! /usr/bin/python
# File: latticematch.py
import sys
# from line_profiler import LineProfiler

def ElemMatch(e1, e2):
  return e1 == e2

# preDic: preDic[e] = [b,c,d] (b->e; c->e; d->e)
def invertEdges(edges, index_cid_sub):
  preDic = {}
  for k in edges:
    for e in edges[k]:
      sub_e = index_cid_sub[e] 
      sub_k = index_cid_sub[k]
      preDic[sub_e].append(sub_k)
  return preDic

def orderedLattice(cids, edges):
  # generate a topological ordered words
  lattice_ordered = []  
  visited = set()
  indegree = {}
  for i in cids:
    indegree[i] = 0
  for k in edges:
    for e in edges[k]:
      if e not in indegree:
        indegree[e] = 0
      indegree[e] += 1
  # print indegree
  for e in indegree:
    if indegree[e] == 0:
      visited.add(e)
  # print visited
  while len(visited) > 0:
    n = visited.pop()  
    lattice_ordered.append(n)
    if n in edges:
      for e in edges[n]:
        indegree[e] -= 1
        if indegree[e] == 0:
          visited.add(e)
  # print lattice_ordered[:20]
  # sys.exit(0)
  return lattice_ordered

# DEBUG function
def PrintStatus(f, path, message=''): 
  # if message != '': print message
  # print 'F score:'
  # print '\n'.join([str(_) for _ in f])
  # print 'Path:'
  # for p in path:
  #   for pairlist in p:
  #     print '[%20s]' % ', '.join([str('(%d,%d)' % pair) for pair in pairlist]),
  #   print ''
  # raw_input()
  pass

################ THE CORE MATCH FUNCTION ##################
# lattice_words: candidates (words in lattice)
# trans_words: transcript words 
# @profile
def Match(lattice_words, trans_words, edges, candidate_ids, index_cid_sub):
  # F: longest matching up to ith element from lattice_words and and jth from trans_words
  n1 = len(lattice_words)
  n2 = len(trans_words)

  print >>sys.stderr, 'N:', n1, n2 # DEBUG
  
  if n1 == 0 or n2 == 0: 
    return 0, [], []
  # f = [[0] * (n2)] * (n1)  # Python array is weird....
  f = [[0] * n2 for _ in range(n1)] # This is correct way, do not give a shallow copy!!  
  # f = { i:{j : 0 for j in range(0, n2)} for i in range(0, n1)}
  # an "array" for each grid in matrix
  print >>sys.stderr,  'F: Init finished!'

  # This is too slow!
  # path = [[[] for _2 in range(n2)] for _ in range(n1)]
  path = [0 for _ in range(n1 * n2)]

  def EncodeSub(i, j):
    return i * n2 + j

  def DecodeSub(sub):
    return sub / n2, sub % n2

  
  print >>sys.stderr,  'Path: Init finished!'

  indegree = {}

  # indegree stores cids
  for i in candidate_ids:
    indegree[i] = 0
  for k in edges:
    for e in edges[k]:
      if e not in indegree:
        indegree[e] = 0
      indegree[e] += 1

  zero_indegree_index = [index_cid_sub[i] for i in indegree if indegree[i] == 0]
  non_zero_indegree_index = [index_cid_sub[i] for i in indegree if indegree[i] != 0]

  # print 'Zero indegree indexes:',zero_indegree_index

  # print >>sys.stderr, 'INIT...' # DEBUG
  # Simpler init
  # Initialize zero-indegree with j=0
  for i_zero in zero_indegree_index:
    for j in range(n2):
      # if ElemMatch(lattice_words[i_zero], trans_words[j]):
      if lattice_words[i_zero] == trans_words[j]:
        f[i_zero][j] = 1
        # path[i_zero][j].append((-1, -1)) # match
        path[i_zero * n2 + j] = (-1, -1)
  
  PrintStatus(f, path, 'Initialization results:')

  # DP; max over predecessors
  # C[i,j] = max over all i'-> i (predecessor) {  f[i', j-1]+ 1{words[i] == transcript[j]}
  #     f[i',j]
  #     f[i,j-1]
  #   }

  print >>sys.stderr, 'Getting ordered lattice...'
  ordered_cids = orderedLattice(candidate_ids, edges)
  print >>sys.stderr,  'Got ordered lattice...'

  # for i_index in range(0, n1):
  for i_cid in ordered_cids:     # Must have topological order for DP
    for j in range(0, n2):
      # i_cid = candidate_ids[i_index]
      i_index = index_cid_sub[i_cid]

      # TODO edges stores cids; i_succ_index is cid!!! i_index is index
      for i_succ_cid in edges[i_cid]:
        i_succ_index = index_cid_sub[i_succ_cid]
        word_succ = lattice_words[i_succ_index]
        if i_succ_index < n1 and j+1 < n2 \
          and word_succ == trans_words[j+1]:
          # and ElemMatch(word_succ, trans_words[j+1]):
            if f[i_succ_index][j+1] < f[i_index][j] + 1:
              f[i_succ_index][j+1] = f[i_index][j] + 1
              # path[i_succ_index][j+1] = [(i_index,j)]    # Path stores index :P
              path[i_succ_index * n2 + j+1] = (i_index,j)

            # elif f[i_succ_index][j+1] == f[i_index][j] + 1: # multipath
            #   path[i_succ_index * n2 + j+1] = (i_index,j)

        if i_succ_index < n1: # shift down (to successor)
          if f[i_succ_index][j] < f[i_index][j]:
            f[i_succ_index][j] = f[i_index][j]
            path[i_succ_index * n2 + j] = (i_index, j)
          # elif f[i_succ_index][j] == f[i_index][j]: # another best path
          #   path[i_succ_index * n2 + j].append((i_index, j))

      if j + 1 < n2: # shift right (to next word in transcript)
        if f[i_index][j+1] < f[i_index][j]:
          f[i_index][j+1] = f[i_index][j]
          path[i_index * n2 + j+1] = (i_index, j)
        # elif f[i_index][j+1] == f[i_index][j]: # another best path
        #   path[i_index * n2 + j+1].append((i_index, j))

  # Only match "diagonal" edges
  possible_opt_match_pairs = []  # can have cases like [(1,a) (2,a)] but have to be both optimal!
  visited = set()

  # Search from end to head for all viable best paths
  def LableMatchDFS(i, j):
    # print 'visiting ',i,j
    if (i, j) in visited:  # prevent multiple adds
      return
    visited.add((i, j))   # mark as visited
    if i >= 0 and j >= 0:  # Terminate at "-1"s
      pair = path[i * n2 + j]
      if pair != 0:
        pi, pj = pair
        # i,j is a valid match: if pi != i, pi must be pred of i
        if pi != i and pj != j:
          possible_opt_match_pairs.append((i, j))

        # Why deeper than max recursion?
        LableMatchDFS(pi, pj)     # continue searching

  # F matrix might look like this:
  # [1, 1, 1]
  # [1, 1, 1]
  # [1, 1, 2]
  # [0, 0, 0]
  # [0, 1, 1]
  # [1, 1, 1]
  # So we should check best end-nodes
  endnodes = [index_cid_sub[i] for i in edges if len(edges[i]) == 0]
  maxscore = 0
  besti = []
  for i in endnodes:
    if maxscore < f[i][n2 - 1]:
      maxscore = f[i][n2 - 1]
      besti = [i]
    elif maxscore == f[i][n2 - 1]:
      besti.append(i)

  # for i in besti:
  #   LableMatchDFS(i, n2 - 1)  # find all best paths

  queue = [(i, n2 - 1) for i in besti]
  nowi = 0
  while nowi != len(queue):
    i, j = queue[nowi]
    nowi += 1
    if (i, j) in visited:  # prevent multiple adds
      continue
    visited.add((i, j))   # mark as visited
    if i >= 0 and j >= 0:  # Terminate at "-1"s
      pair = path[i * n2 + j]
      if pair != 0:
        pi, pj = pair
        # i,j is a valid match: if pi != i, pi must be pred of i
        if pi != i and pj != j:
          possible_opt_match_pairs.append((i, j))
        queue.append((pi, pj))

  return maxscore, [x for x in reversed(possible_opt_match_pairs)], path, f

