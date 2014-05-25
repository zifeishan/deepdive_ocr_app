#! /usr/bin/bash

'''
This script aggregates supervision sequence into a single line,
for compression when loading into database.
'''

import sys, os

dbname = 'ddocr'
path = ''
doclist = ''
if len(sys.argv) == 2:
  path = sys.argv[1]
else:
  print 'Usage:',sys.argv[0],'SUPV_DIR'
  sys.exit(1)

files = os.listdir(path)

for filename in files:
  if not filename.endswith('.seq'):
    continue
  docid = filename[:-len('.seq')]
  print 'Loading', docid
  filepath = path + '/' + docid + '.seq'
  if not os.path.exists(filepath):
    print 'PATH NOT EXISTS:', filepath
    continue

  content = '~^~'.join([l.rstrip('\n') for l in open(filepath).readlines()])
  tmpoutfile = path + '/'+ docid  + '.seq_aggregated'
  fout = open(tmpoutfile, 'w')

  print >>fout, docid+'\t'+content
  fout.close()
