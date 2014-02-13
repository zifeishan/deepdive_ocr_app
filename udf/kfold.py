#! /usr/bin/env python

# Call: /udf/kfold.py "${KFOLD_NUM}" "${KFOLD_ITER}"filtered_labels label_t label_c

import os, sys

# DEBUG
print sys.argv

if len(sys.argv) >= 5:
  KFOLD_NUM = sys.argv[1]
  KFOLD_ITER = sys.argv[2]
  table = sys.argv[3]
  remove_vars = sys.argv[4:]

else:
  print 'Usage:',sys.argv[0],'KFOLD_NUM KFOLD_ITER temporal_table_to_fold query_col_1 query_col_2 ...'
  sys.exit(1)

sql_queries = []
numrows = 'select count(*) from ' + table


# K-fold query: hold out columns with ID from (i-1)/K to i/K
updatequery = ' '.join(
  ['UPDATE', table, 'SET', 
   ','.join([var + '= NULL' for var in remove_vars]),
   'where id < ('+ numrows + ') * ' + KFOLD_ITER + ' / '
   + KFOLD_NUM + ' and id >= ('+ numrows + ') * (' + 
    KFOLD_ITER + ' - 1) / '+ KFOLD_NUM + ';'])

sql_queries.append(updatequery)
fullquery = 'psql -c """'+'\n'.join(sql_queries)+'""" '+os.environ['DBNAME']
os.system(fullquery)

# DEBUG
print fullquery