[JOURNAL_13730]  SCORE: 2586 / 5000 (0.517200), matches: 2586 / 5000
         68230917 function calls in 13.788 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.312    0.312   13.788   13.788 ext_sup_orderaware_new_tsv.py:3(<module>)
        1   12.469   12.469   13.437   13.437 latticematch_singlepath.py:61(Match)
 31838633    0.447    0.000    0.447    0.000 latticematch_singlepath.py:5(ElemMatch)
 36310877    0.440    0.000    0.440    0.000 latticematch_singlepath.py:80(EncodeSub)
        1    0.058    0.058    0.066    0.066 latticematch_singlepath.py:18(orderedLattice)
     6367    0.014    0.000    0.020    0.000 ext_sup_orderaware_new_tsv.py:38(AddEdge)
    19780    0.012    0.000    0.012    0.000 {method 'append' of 'list' objects}
     2593    0.007    0.000    0.007    0.000 {method 'split' of 'str' objects}
    10820    0.006    0.000    0.006    0.000 {method 'add' of 'set' objects}
    15844    0.005    0.000    0.005    0.000 {len}
    13700    0.005    0.000    0.005    0.000 {method 'strip' of 'str' objects}
        1    0.004    0.004    0.004    0.004 {method 'readlines' of 'file' objects}
     5009    0.004    0.000    0.004    0.000 {range}
     5000    0.002    0.000    0.002    0.000 {method 'pop' of 'set' objects}
     2228    0.002    0.000    0.002    0.000 {method 'join' of 'str' objects}


[JOURNAL_13730]  SCORE: 2586 / 5000 (0.517200), matches: 2586 / 5000
         31920040 function calls in 12.791 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.297    0.297   12.791   12.791 ext_sup_orderaware_new_tsv.py:3(<module>)
        1   11.892   11.892   12.454   12.454 latticematch_singlepath.py:61(Match)
 31838633    0.482    0.000    0.482    0.000 latticematch_singlepath.py:5(ElemMatch)
        1    0.058    0.058    0.065    0.065 latticematch_singlepath.py:18(orderedLattice)
     6367    0.012    0.000    0.017    0.000 ext_sup_orderaware_new_tsv.py:38(AddEdge)
     2593    0.012    0.000    0.012    0.000 {method 'split' of 'str' objects}
    19780    0.011    0.000    0.011    0.000 {method 'append' of 'list' objects}
    10820    0.007    0.000    0.007    0.000 {method 'add' of 'set' objects}
    13700    0.005    0.000    0.005    0.000 {method 'strip' of 'str' objects}
    15844    0.004    0.000    0.004    0.000 {len}


[JOURNAL_13730]  SCORE: 2586 / 5000 (0.517200), matches: 2586 / 5000
         81407 function calls in 10.148 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.294    0.294   10.148   10.148 ext_sup_orderaware_new_tsv.py:3(<module>)
        1    9.741    9.741    9.814    9.814 latticematch_singlepath.py:61(Match)
        1    0.053    0.053    0.060    0.060 latticematch_singlepath.py:18(orderedLattice)
     6367    0.012    0.000    0.017    0.000 ext_sup_orderaware_new_tsv.py:38(AddEdge)
     2593    0.012    0.000    0.012    0.000 {method 'split' of 'str' objects}
    19780    0.011    0.000    0.011    0.000 {method 'append' of 'list' objects}
    10820    0.007    0.000    0.007    0.000 {method 'add' of 'set' objects}
    13700    0.005    0.000    0.005    0.000 {method 'strip' of 'str' objects}
    15844    0.004    0.000    0.004    0.000 {len}



===================

Match function:


Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    62                                           @profile
    63                                           def Match(lattice_words, trans_words, edges, candidate_ids, index_cid_sub):
    64                                             # F: longest matching up to ith element from lattice_words and and jth from trans_words
    65         1            8      8.0      0.0    n1 = len(lattice_words)
    66         1            2      2.0      0.0    n2 = len(trans_words)
    67
    68         1           54     54.0      0.0    print >>sys.stderr, 'N:', n1, n2 # DEBUG
    69
    70         1            3      3.0      0.0    if n1 == 0 or n2 == 0:
    71                                               return 0, [], []
    72                                             # f = [[0] * (n2)] * (n1)  # Python array is weird....
    73      2001        69110     34.5      0.0    f = [[0] * n2 for _ in range(n1)] # This is correct way, do not give a shallow copy!!
    74                                             # f = { i:{j : 0 for j in range(0, n2)} for i in range(0, n1)}
    75                                             # an "array" for each grid in matrix
    76         1           41     41.0      0.0    print >>sys.stderr,  'F: Init finished!'
    77
    78                                             # This is too slow!
    79                                             # path = [[[] for _2 in range(n2)] for _ in range(n1)]
    80   4000001      8628513      2.2      5.9    path = [0 for _ in range(n1 * n2)]
    81
    82         1           10     10.0      0.0    def EncodeSub(i, j):
    83                                               return i * n2 + j
    84
    85         1            3      3.0      0.0    def DecodeSub(sub):
    86                                               return sub / n2, sub % n2
    87
    88
    89         1           27     27.0      0.0    print >>sys.stderr,  'Path: Init finished!'
    90
    91         1            5      5.0      0.0    indegree = {}
    92
    93                                             # indegree stores cids
    94      2001         4068      2.0      0.0    for i in candidate_ids:
    95      2000         4451      2.2      0.0      indegree[i] = 0
    96      2001         4220      2.1      0.0    for k in edges:
    97      4505        10048      2.2      0.0      for e in edges[k]:
    98      2505         5470      2.2      0.0        if e not in indegree:
    99                                                   indegree[e] = 0
   100      2505         5730      2.3      0.0        indegree[e] += 1
   101
   102      2001         4201      2.1      0.0    zero_indegree_index = [index_cid_sub[i] for i in indegree if indegree[i] == 0]
   103      2001         4650      2.3      0.0    non_zero_indegree_index = [index_cid_sub[i] for i in indegree if indegree[i] != 0]
   104
   105                                             # print 'Zero indegree indexes:',zero_indegree_index
   106
   107                                             # print >>sys.stderr, 'INIT...' # DEBUG
   108                                             # Simpler init
   109                                             # Initialize zero-indegree with j=0
   110         3            9      3.0      0.0    for i_zero in zero_indegree_index:
   111      4002         8739      2.2      0.0      for j in range(n2):
   112                                                 # if ElemMatch(lattice_words[i_zero], trans_words[j]):
   113      4000         9184      2.3      0.0        if lattice_words[i_zero] == trans_words[j]:
   114                                                   f[i_zero][j] = 1
   115                                                   # path[i_zero][j].append((-1, -1)) # match
   116                                                   path[i_zero * n2 + j] = (-1, -1)
   117
   118         1            9      9.0      0.0    PrintStatus(f, path, 'Initialization results:')
   119
   120                                             # DP; max over predecessors
   121                                             # C[i,j] = max over all i'-> i (predecessor) {  f[i', j-1]+ 1{words[i] == transcript[j]}
   122                                             #     f[i',j]
   123                                             #     f[i,j-1]
   124                                             #   }
   125
   126         1           33     33.0      0.0    print >>sys.stderr, 'Getting ordered lattice...'
   127         1        15711  15711.0      0.0    ordered_cids = orderedLattice(candidate_ids, edges)
   128         1           32     32.0      0.0    print >>sys.stderr,  'Got ordered lattice...'
   129
   130                                             # for i_index in range(0, n1):
   131      1715         4088      2.4      0.0    for i_cid in ordered_cids:     # Must have topological order for DP
   132   3430782      7674087      2.2      5.3      for j in range(0, n2):
   133                                                 # i_cid = candidate_ids[i_index]
   134   3429068      7817542      2.3      5.4        i_index = index_cid_sub[i_cid]
   135
   136                                                 # TODO edges stores cids; i_succ_index is cid!!! i_index is index
   137   7764136     19049093      2.5     13.1        for i_succ_cid in edges[i_cid]:
   138   4335068      9855703      2.3      6.8          i_succ_index = index_cid_sub[i_succ_cid]
   139   4335068      9570136      2.2      6.6          word_succ = lattice_words[i_succ_index]
   140   4335068     10278414      2.4      7.1          if i_succ_index < n1 and j+1 < n2 \
   141   4332901     10288468      2.4      7.1            and word_succ == trans_words[j+1]:
   142                                                     # and ElemMatch(word_succ, trans_words[j+1]):
   143     46204       116688      2.5      0.1              if f[i_succ_index][j+1] < f[i_index][j] + 1:
   144     44625       111964      2.5      0.1                f[i_succ_index][j+1] = f[i_index][j] + 1
   145                                                         # path[i_succ_index][j+1] = [(i_index,j)]    # Path stores index :P
   146     44625       119895      2.7      0.1                path[i_succ_index * n2 + j+1] = (i_index,j)
   147
   148                                                       # elif f[i_succ_index][j+1] == f[i_index][j] + 1: # multipath
   149                                                       #   path[i_succ_index * n2 + j+1] = (i_index,j)
   150
   151   4335068      9785221      2.3      6.7          if i_succ_index < n1: # shift down (to successor)
   152   4335068     10428096      2.4      7.2            if f[i_succ_index][j] < f[i_index][j]:
   153   3642702      8700459      2.4      6.0              f[i_succ_index][j] = f[i_index][j]
   154   3642702      9287812      2.5      6.4              path[i_succ_index * n2 + j] = (i_index, j)
   155                                                     # elif f[i_succ_index][j] == f[i_index][j]: # another best path
   156                                                     #   path[i_succ_index * n2 + j].append((i_index, j))
   157
   158   3429068      8031628      2.3      5.5        if j + 1 < n2: # shift right (to next word in transcript)
   159   3427354      8794307      2.6      6.1          if f[i_index][j+1] < f[i_index][j]:
   160   1241273      3096256      2.5      2.1            f[i_index][j+1] = f[i_index][j]
   161   1241272      3349475      2.7      2.3            path[i_index * n2 + j+1] = (i_index, j)
   162                                                   # elif f[i_index][j+1] == f[i_index][j]: # another best path
   163                                                   #   path[i_index * n2 + j+1].append((i_index, j))
   164
   165                                             # Only match "diagonal" edges
   166                                             possible_opt_match_pairs = []  # can have cases like [(1,a) (2,a)] but have to be both optimal!
   167                                             visited = set()
   168
   169                                             # Search from end to head for all viable best paths
   170                                             def LableMatchDFS(i, j):
   171                                               # print 'visiting ',i,j
   172                                               if (i, j) in visited:  # prevent multiple adds
   173                                                 return
   174                                               visited.add((i, j))   # mark as visited
   175                                               if i >= 0 and j >= 0:  # Terminate at "-1"s
   176                                                 pair = path[i * n2 + j]
   177                                                 if pair != 0:
   178                                                   pi, pj = pair
   179                                                   # i,j is a valid match: if pi != i, pi must be pred of i
   180                                                   if pi != i and pj != j:
   181                                                     possible_opt_match_pairs.append((i, j))
   182
   183                                                   # Why deeper than max recursion?
   184                                                   LableMatchDFS(pi, pj)     # continue searching
   185
   186                                             # F matrix might look like this:
   187                                             # [1, 1, 1]
   188                                             # [1, 1, 1]
   189                                             # [1, 1, 2]
   190                                             # [0, 0, 0]
   191                                             # [0, 1, 1]
   192                                             # [1, 1, 1]
   193                                             # So we should check best end-nodes
   194                                             endnodes = [index_cid_sub[i] for i in edges if len(edges[i]) == 0]
   195                                             maxscore = 0
   196                                             besti = []
   197                                             for i in endnodes:
   198                                               if maxscore < f[i][n2 - 1]:
   199                                                 maxscore = f[i][n2 - 1]
   200                                                 besti = [i]
   201                                               elif maxscore == f[i][n2 - 1]:
   202                                                 besti.append(i)
   203
   204                                             # for i in besti:
   205                                             #   LableMatchDFS(i, n2 - 1)  # find all best paths
   206
   207                                             queue = [(i, n2 - 1) for i in besti]
   208                                             nowi = 0
   209                                             while nowi != len(queue):
   210                                               i, j = queue[nowi]
   211                                               nowi += 1
   212                                               if (i, j) in visited:  # prevent multiple adds
   213                                                 continue
   214                                               visited.add((i, j))   # mark as visited
   215                                               if i >= 0 and j >= 0:  # Terminate at "-1"s
   216                                                 pair = path[i * n2 + j]
   217                                                 if pair != 0:
   218                                                   pi, pj = pair
   219                                                   # i,j is a valid match: if pi != i, pi must be pred of i
   220                                                   if pi != i and pj != j:
   221                                                     possible_opt_match_pairs.append((i, j))
   222                                                   queue.append((pi, pj))
   223
   224                                             return maxscore, [x for x in reversed(possible_opt_match_pairs)], path, f

