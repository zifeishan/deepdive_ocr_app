#! /usr/bin/python

# SAMPLE USAGE:
# python ./prepare_ngram_data.py /lfs/local/0/zifei/google-ngram/output/

import os, sys

if __name__ == "__main__": 
  # ...
  if len(sys.argv) >= 3:
    path = sys.argv[1]
    table_name = sys.argv[2]
    if len(sys.argv) >= 4:
      dbname = sys.argv[3]
    else:
      dbname = 'ddocr'

  else:
    print 'Usage:',sys.argv[0],'<ngram-dir> <table_name> <dbname>'
    print 'e.g.: ',sys.argv[0],'/lfs/local/0/zifei/google-ngram/output/ ngram_1'
    sys.exit(1)

  files = [f for f in os.listdir(path) if f.endswith('.ngram')]
  print files[:10],'...'
  pq = 'drop table if exists '+table_name + ';'
  os.system('psql -c "'+pq+'" '+dbname)

  pq = 'create table '+table_name+'''(
    id BIGSERIAL PRIMARY KEY,
    gram TEXT,
    count REAL);''' 
  print pq
    
  os.system('psql -c "'+pq+'" '+dbname)

  # Create error table
  pq = '''CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea)'''
  print pq
  os.system('psql -c "'+pq+'" '+dbname)

  # Copy and neglect errors
  for f in files:
    fpath = os.path.abspath(path+'/'+f)
    print 'Copying file:'+ fpath
    pq = 'COPY '+table_name+'(gram, count) FROM \''+fpath+'\' LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;'
    # Ignore (at most 1k) errors and put errors into table err
    os.system('psql -c "'+pq+'" '+dbname)

  print 'Done.'
