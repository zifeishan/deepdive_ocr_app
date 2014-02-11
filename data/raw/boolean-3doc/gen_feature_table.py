#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys   # needed by most
import random   # random 
import yaml     # yaml parsing
import pprint   # pretty print

dirbase = './'
ids = [f.rstrip('.output.txt') for f in os.listdir(dirbase) if f.endswith('.output.txt')]
print 'Process files:', ids


fout = open('feature_table.csv', 'w')
for fid in ids:
  lines = open(dirbase + fid+'.output.txt').readlines()

  for l in lines: 
    p = l.strip().split('\t')
    if len(p) <= 1: continue

    tword = p[1] 
    cword = p[2]

    sw_t = CheckNGram(tword, 1)
    sw_c = CheckNGram(cword, 1)
    
    features = {}

    if sw_t > sw_c:
      features['1gramMore_T'] = True
    else:
      features['1gramMore_T'] = False
    if sw_t > 0:
      features['1gram_T'] = True
    else:
      features['1gram_T'] = False
    if sw_c > 0:
      features['1gram_C'] = True
    else:
      features['1gram_C'] = False


    vals = [features[b] for b in features]
    
    # print vals
    for sub in range(0, len(vals)):
      print >>fout, str(wid) + ',' + str(sub)+','+ str(vals[sub])
    wid += 1

    names = [n for n in features] ### TODO print names...


totid = wid

wid = 1
fl1 = open('label1_table.csv', 'w')
fl2 = open('label2_table.csv', 'w')
for fid in ids:
  labels = [int(s) for s in open(dirbase + fid+'.labels.txt').readlines()]
  for l in labels: 
    l1 = False
    l2 = False
    if l == 1: l1 = True
    if l == 2: l2 = True
    print >>fl1, str(wid) + ',' + str(l1)
    print >>fl2, str(wid) + ',' + str(l2)
    wid += 1

fl1.close()
fl2.close()

