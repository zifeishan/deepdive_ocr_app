#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys   # needed by most
import random   # random 


if __name__ == "__main__": 
  if len(sys.argv) == 3:
    path = sys.argv[1]
    outpath = sys.argv[2]
  else:
    print 'Usage:',sys.argv[0],'<gram-path> <outpath>'
    sys.exit(1)

  # files = [f for f in os.listdir(dirpath) if f.startswith('googlebooks-eng-all')]

  # for f in files:

  f = path
  fpath = path
  fid = f.split('-')[-1]
  # fpath = dirpath + '/' + f 
  fin = open(fpath)
  fout = open(outpath, 'a')

  line = fin.readline()
  parts = line.split('\t')
  ngram = parts[0]
  count = int(parts[-2])

  linenum = 1
  currentword = ngram
  currentcount = count

  while True:
    line = fin.readline()
    if line == "": break

    parts = line.split('\t')
    ngram = parts[0]
    count = int(parts[-2])
    if ngram == currentword:
      currentcount += count
    else:
      print >>fout, currentword+'\t'+str(currentcount)
      currentword = ngram
      currentcount = count


    linenum += 1
    if linenum % 10000000 == 0:
      print 'Processing line', linenum

  # RM!!!!!!!!!!!
  os.remove(path)
