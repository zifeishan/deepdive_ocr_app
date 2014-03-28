psql -c """update candidate
	set label = true
	where id in (select candidate_id from orderaware_supv_label where label = true);
""" $DB_NAME

psql -c """update candidate set label = false where label is null;
""" $DB_NAME

echo 'TODO fix: supv document not found!!'

# #############################
# # HOLD OUT
# psql -c """update candidate 
#   set label = null 
#   where docid in (select docid from eval_docs);""" $DB_NAME
