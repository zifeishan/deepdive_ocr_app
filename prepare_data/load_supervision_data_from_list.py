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
  print 'e.g. python load_aligned_ocr_outputs_from_list.py ddocr_1k /lfs/local/0/zifei/deepdive/app/ocr/data/supervision/supervision-data/ ../data/doclist-1k.txt'
  sys.exit(1)


ids = [s.strip() for s in open(doclist).readlines()]

###################

os.system('''
psql -c "DROP TABLE IF EXISTS html_1gram CASCADE;" '''+dbname+'''
psql -c "DROP TABLE IF EXISTS html_2gram CASCADE;" '''+dbname+'''
psql -c "DROP TABLE IF EXISTS html_3gram CASCADE;" '''+dbname+'''
''')

os.system('''
# Create error table
psql -c """DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);""" '''+dbname+'''
''')

os.system('''
psql -c "create table html_1gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, freq INT);" '''+dbname+'''
''')
os.system('''
psql -c "create table html_2gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, word2 TEXT, freq INT); " '''+dbname+'''
''')

os.system('''
psql -c "create table html_3gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, word2 TEXT, word3 TEXT, freq INT); " '''+dbname+'''
''')

for docid in ids:
  filepath = path + '/' + docid + '.1gram'
  if not os.path.exists(filepath):
    print 'PATH NOT EXISTS:', filepath
    continue
  
  for thisgram in ['.1gram', '.2gram', '.3gram']:
    filepath = path + '/' + docid + thisgram
    print filepath
    os.system('''sed \'s/\\\\/\\\\\\\\/g\' '''+filepath+''' | psql -c "COPY html_1gram(docid, freq, word1) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" '''+ dbname)
