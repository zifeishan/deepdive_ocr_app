#############################
# HOLD OUT
psql -c """update candidate 
  set label = null 
  where docid in (select docid from eval_docs);""" $DB_NAME
