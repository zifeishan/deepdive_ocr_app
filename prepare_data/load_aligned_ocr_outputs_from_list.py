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
os.system('''psql -c """create table cand_word(id BIGSERIAL PRIMARY KEY, 
  candidate_id BIGSERIAL,
  docid TEXT,
  varid INT, -- start from 1
  candid INT, -- start from 0, multinomial, according to source
  source TEXT, -- 1-1 mapping to source
  wordid INT, -- start from 0
  word TEXT,
  page INT, 
  l INT, 
  t INT, 
  r INT, 
  b INT,  
  pos TEXT,
  ner TEXT,
  stem TEXT);""" '''+dbname)

for docid in ids:
  filepath = path + '/' + docid + '.cand_word'
  if not os.path.exists(filepath):
    print 'PATH NOT EXISTS:', filepath
    continue
  print 'Loading', docid
  os.system('''sed \'s/\\\\/\\\\\\\\/g\' '''+filepath+''' | psql -c "COPY cand_word(docid, varid, candid, source, wordid, word, page, l, t, r, b, pos, ner, stem) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" '''+ dbname)


os.system('''
  # Variable table
  psql -c "drop table if exists variable cascade;" '''+dbname+'''
  psql -c """create table variable(id BIGSERIAL PRIMARY KEY, 
    docid TEXT,
    varid INT,
    label INT);""" '''+dbname+'''
  psql -c """insert into variable(docid, varid) select distinct docid, varid from cand_word order by docid, varid;""" '''+dbname+'''

  # Candidate table
  psql -c "drop table if exists candidate cascade;" '''+dbname+'''
  psql -c """create table candidate(id BIGSERIAL PRIMARY KEY, 
    variable_id BIGSERIAL,
    docid TEXT, -- redundancy
    varid INT,  -- redundancy
    candid INT,
    source TEXT,
    label BOOLEAN);""" '''+dbname+'''
  psql -c """insert into candidate(variable_id, docid, varid, candid, source) 
    select distinct variable.id as variable_id, variable.docid, variable.varid, candid, source
    from cand_word, variable 
      where variable.docid = cand_word.docid
        and variable.varid = cand_word.varid
    order by variable_id, candid, source;
    """ '''+dbname+'''

  # Update cand_word
  psql -c """update cand_word 
    set candidate_id = candidate.id
    from candidate
    where cand_word.docid = candidate.docid
      and cand_word.varid = candidate.varid
      and cand_word.candid = candidate.candid
    ;
  """ '''+dbname+'''
  ''')

