#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys   # needed by most
import random   # random 
import yaml     # yaml parsing
import pprint   # pretty print

dirbase = 'boolean-f52-c3-m620/'
ids = [f.rstrip('.features.txt') for f in os.listdir(dirbase) if f.endswith('.features.txt')]
print 'Process files:', ids

wid = 1
fout = open('feature_table.csv', 'w')
for fid in ids:
  lines = open(dirbase + fid+'.features.txt').readlines()
  for l in lines: 
    vals = [b for b in l.strip().split('\t')]
    # print vals
    for sub in range(0, len(vals)):
      print >>fout, str(wid) + ',' + str(sub)+','+ str(vals[sub])
    wid += 1

totid = wid

wid = 1
flT = open('labelT_table.csv', 'w')
flC = open('labelC_table.csv', 'w')
for fid in ids:
  labels = [s for s in open(dirbase + fid+'.labels.txt').readlines()]
  # T vs C
  options = [s.strip().split('\t') for s in open(dirbase + fid+'.options.txt').readlines()]
  # print options
  for l in labels: 
    lT = False
    lC = False
    if l == 'Tesseract': lT = True
    if l == 'Cuneiform': lC = True
    # DocID, WordID, Label
    print >>flT, str(fid) + ',' + str(wid) + ',' + str(lT)
    print >>flC, str(fid) + ',' + str(wid) + ',' + str(lC)
    wid += 1

flT.close()
flC.close()

