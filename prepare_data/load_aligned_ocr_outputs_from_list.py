#! /usr/bin/python
# Sample usage: <this> <html_path> <outbase>
# NEW: ignore existing files in output dir

import codecs

import sys, os

dbname = 'ddocr'
path = ''
doclist = ''
if len(sys.argv) == 4:
  dbname = sys.argv[1]
  path = sys.argv[2]
  doclist = sys.argv[3]
else:
  print 'Usage:',sys.argv[0],'DBNAME CAND_DIR DOCID_LIST'
  print 'e.g. python load_aligned_ocr_outputs_from_list.py ddocr_1k /dfs/madmax/0/zifei/deepdive/app/ocr/data/journals-output/ ../data/doclist-1k.txt'
  sys.exit(1)


ids = [s.strip() for s in open(doclist).readlines()]

os.system('''psql -c """DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);""" '''+dbname)
os.system('''psql -c "drop table if exists cand_word CASCADE;" '''+dbname)
os.system('''psql -c """
  CREATE TABLE cand_word(
    cand_word_id  TEXT,
    candidate_id  TEXT,
    docid         TEXT,
    varid         INT,      -- start from 1
    candid        INT,      -- start from 0, according to source
    source        TEXT,     -- 1-1 mapping to source
    wordid        INT,      -- start from 0
    word          TEXT,
    page          INT, 
    l             INT, 
    t             INT, 
    r             INT, 
    b             INT,  
    pos           TEXT,
    ner           TEXT,
    stem          TEXT)
  DISTRIBUTED BY (docid);""" '''+dbname)

for docid in ids:
  filepath = path + '/' + docid + '.cand_word'
  if not os.path.exists(filepath):
    print 'PATH NOT EXISTS:', filepath
    continue
  print 'Loading', docid
  os.system('''sed \'s/\\\\/\\\\\\\\/g\' '''+filepath+''' | psql -c "COPY cand_word(docid, varid, candid, source, wordid, word, page, l, t, r, b, pos, ner, stem) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" '''+ dbname)

