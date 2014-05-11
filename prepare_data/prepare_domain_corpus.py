#! /usr/bin/bash

import sys, os

dbname = 'ddocr'
path = ''
doclist = ''
if len(sys.argv) == 3:
  dbname = sys.argv[1]
  path = sys.argv[2]
else:
  print 'Usage:',sys.argv[0],'DBNAME SUPV_DIR'
  print 'e.g. python %s ddocr_100 /dfs/madmax/0/zifei/deepdive/app/ocr/data/supervision/' % (sys.argv[0])
  sys.exit(1)

os.system('''
psql -c "DROP TABLE IF EXISTS domain_corpus_seq CASCADE;" '''+dbname+'''
''')

os.system('''
# Create error table
psql -c """DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);""" '''+dbname+'''
''')

os.system('''
psql -c """create table domain_corpus_seq(
    doc_id  BIGINT,
    wordid BIGSERIAL,
    word   TEXT) 
    DISTRIBUTED BY (doc_id); """ '''+dbname+'''
''')

doc_id = 1
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

  os.system('''sed \'s/\\\\/\\\\\\\\/g\' '''+filepath+''' | sed \'s/$/\\t%d/\' | psql -c "COPY domain_corpus_seq(word, doc_id) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" ''' % (doc_id)+ dbname)
  doc_id += 1

os.system('''psql -c "ANALYZE domain_corpus_seq;" '''+dbname)
