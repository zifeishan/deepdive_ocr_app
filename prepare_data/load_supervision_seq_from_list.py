#! /usr/bin/python
# Sample usage: <this> <html_path> <outbase>
# NEW: ignore existing files in output dir

import sys, os

dbname = 'ddocr'
path = ''
doclist = ''
if len(sys.argv) == 4:
  dbname = sys.argv[1]
  path = sys.argv[2]
  doclist = sys.argv[3]
else:
  print 'Usage:',sys.argv[0],'DBNAME SUPV_DIR DOCID_LIST'
  print 'e.g. python load_aligned_ocr_outputs_from_list.py ddocr_100 /dfs/madmax/0/zifei/deepdive/app/ocr/data/supervision/ ../data/doclist/doclist-100.txt'
  sys.exit(1)


ids = [s.strip() for s in open(doclist).readlines()]

###################

os.system('''
psql -c "DROP TABLE IF EXISTS html_seq CASCADE;" '''+dbname+'''
''')

os.system('''
# Create error table
psql -c """DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);""" '''+dbname+'''
''')

os.system('''
psql -c """create table html_seq(
    docid  TEXT,
    wordid BIGSERIAL,
    word   TEXT) 
    DISTRIBUTED BY (docid); """ '''+dbname+'''
''')

for docid in ids:
  print 'Loading', docid
  filepath = path + '/' + docid + '.seq'
  if not os.path.exists(filepath):
    print 'PATH NOT EXISTS:', filepath
    continue

  os.system('''sed \'s/\\\\/\\\\\\\\/g\' '''+filepath+''' | sed \'s/$/\\t%s/\' | psql -c "COPY html_seq(word, docid) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" ''' % (docid)+ dbname)

os.system('''psql -c "ANALYZE html_seq;" '''+dbname)
