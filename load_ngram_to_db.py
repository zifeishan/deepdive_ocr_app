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

  for f in files:
    fpath = os.path.abspath(path+'/'+f)
    print 'Copying file:'+ fpath
    pq = 'COPY '+table_name+'(gram, count) FROM \''+fpath+'\''
    os.system('psql -c "'+pq+'" '+dbname)

  print 'Done.'
