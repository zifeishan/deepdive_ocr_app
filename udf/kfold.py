#! /usr/bin/env python

# Call: /udf/kfold.py "${KFOLD_NUM}" "${KFOLD_ITER}"filtered_labels label_t label_c

import os, sys

# DEBUG
print sys.argv

# TODO Check if right dbname??
def ExecSQL(query):
  os.system('psql -c "'+query+'";')

if len(sys.argv) >= 5:
  KFOLD_NUM = sys.argv[1]
  KFOLD_ITER = sys.argv[2]
  table = sys.argv[3]
  remove_vars = sys.argv[4:]

else:
  print 'Usage:',sys.argv[0],'KFOLD_NUM KFOLD_ITER temporal_table_to_fold query_col_1 query_col_2 ...'
  sys.exit(1)

sql_queries = []
sql_queries.append('\set foldnum '+KFOLD_NUM)
sql_queries.append('\set thisfold 1'+KFOLD_ITER)
sql_queries.append("\set numrows \'select count(*) from " + table + "\'")

# K-fold query: hold out columns with ID from (i-1)/K to i/K
updatequery = ' '.join(
  ['UPDATE', table, 'SET', 
   ','.join([var + '= NULL' for var in remove_vars]),
   'where id < (:numrows) * :thisfold / :foldnum and id >= (:numrows) * (:thisfold - 1) / :foldnum;'])

sql_queries.append(updatequery)
os.system('psql -c """'+'\n'.join(sql_queries)+'""" ddocr')
# ExecSQL(updatequery)

# DEBUG
print 'psql -c """'+'\n'.join(sql_queries)+'""" ddocr'