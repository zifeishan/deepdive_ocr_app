#! /usr/bin/python

import os, sys

files = os.listdir(".")

# print files

for f in files:
  path = f + '/'
  if not os.path.exists(path):
    continue
  subfiles = [s for s in os.listdir(path) if s.endswith('.tsv')]
  for subfile in subfiles:
    tsv = path + subfile
    # print tsv
    lines = [l.strip().split('\t') for l in open(tsv).readlines()]
    print tsv
    # print lines
    # for 

