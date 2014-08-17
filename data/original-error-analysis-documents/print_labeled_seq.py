#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys   # needed by most
import random   # random 
import yaml     # yaml parsing
import pprint   # pretty print

if __name__ == "__main__": 
  # ...
  if len(sys.argv) == 2:
    path = sys.argv[1]
  else:
    print 'Usage:',sys.argv[0],'<file>'
    sys.exit(1)

  lines = [l.rstrip('\n') for l in open(path).readlines()]

  print path
  fout = open(path+'.seq', 'w')

  for l in lines: 
    if len(l) == 0: # empty line
      # print >>fout, l
      continue

    w1 = l[3:18].strip(' ') 
    w2 = l[19:19+15].strip(' ')
      
    if '|||' in l or '///' in l:  # already tagged
      if '$' not in l: 
        print l
        continue
      words = l.split('$')[1:]
      if len(words) == 1:
        if words[0] == '': continue
        elif words[0] == '1': 
          print >>fout, w1
        elif words[0] == '2':
          print >>fout, w2
        else:
          print >>fout, words[0]
      else:
        for w in words: 
          print >>fout, w
    else:
      if w1 != w2:
        l = l + '///'
        print >>fout, l
      else: 
        print >>fout, w1.strip()
            
  fout.close()
