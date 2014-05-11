psql -c """update candidate
	set label = true
	where id in (select candidate_id from orderaware_supv_label where label = true);
""" $DB_NAME

# Only update docs where we have supervision data
psql -c """update candidate set label = false where label is null and docid in (select distinct docid from orderaware_supv_label);
""" $DB_NAME


# #############################
# # HOLD OUT
# psql -c """update candidate 
#   set label = null 
#   where docid in (select docid from eval_docs);""" $DB_NAME
