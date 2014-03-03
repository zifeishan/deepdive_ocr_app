#! /usr/bin/python

import os, sys

def ElemMatch(e1, e2):
  return e1 == e2

def Match(arr1, arr2):
  # F: longest matching up to ith element from arr1 and and jth from arr2
  n1 = len(arr1)
  n2 = len(arr2)
  if n1 == 0 or n2 == 0: return 0
  # f = [[0] * (n2)] * (n1)  # Python array is weird....
  f = [[0] * n2 for _ in range(n1)] # This is correct way, do not give a shallow copy!!

  # f = { i:{j : 0 for j in range(0, n2)} for i in range(0, n1)}

  # print f
  # Init
  if ElemMatch(arr1[0], arr2[0]):
    f[0][0] = 1

  for i in range(1, n1):
    if ElemMatch(arr1[i], arr2[0]) or f[i-1][0] == 1:
      f[i][0] = 1

  for j in range(1, n2):
    if ElemMatch(arr1[0], arr2[j]) or f[0][j-1] == 1:
      f[0][j] = 1

  # DP
  for i in range(0, n1):
    for j in range(0, n2):
      if i + 1 < n1 and j + 1 < n2 \
        and ElemMatch(arr1[i+1], arr2[j+1]) \
        and f[i+1][j+1] < f[i][j] + 1:
        f[i+1][j+1] = f[i][j] + 1

      if i + 1 < n1 and f[i+1][j] < f[i][j]: # left shift
         f[i+1][j] = f[i][j]

      if j + 1 < n2 and f[i][j+1] < f[i][j]: # right shift
         f[i][j+1] = f[i][j]

  # for i in range(0, n1): 
  #   for j in range(0, n2):
  #     print '(%d,%d): %d\t' % (i,j,f[i][j]),
  return f[n1 - 1][n2 - 1]




if __name__ == "__main__": 
  if len(sys.argv) == 3:
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    arr1 = [l.strip() for l in open(f1).readlines()]
    arr2 = [l.strip() for l in open(f2).readlines()]
    print Match(arr1, arr2)

  else:
    print 'Usage:',sys.argv[0],'<path1> <path2> (words split by \\n)'
    print 'Tetsing:'
    print Match([1],[5,1,2])

    tess = [l.strip().split('\t')[-1] for l in open('../data/journals-test-output/JOURNAL_102371.cand').readlines()]
    lines = [l.strip() for l in open('../data/test-supervision/JOURNAL_102371.seq').readlines()]
    print 'Matching 1000 words:'
    print Match(tess[:1000], lines[:1000])
    print 'Matching all words:', len(tess), len(lines)
    print Match(tess, lines)
    # sys.exit(1)


