#! /usr/bin/env bash

# psql -c """create table cand_2gram(id BIGSERIAL PRIMARY KEY, 
#   cand_word_id BIGSERIAL,
#   feature_gram TEXT);""" $DB_NAME

psql -c "drop table if exists cand_2gram_positive cascade;" $DB_NAME
psql -c "drop table if exists cand_2gram_somepos_candidates cascade;" $DB_NAME
psql -c "drop table if exists cand_2gram_someneg_candidates cascade;" $DB_NAME

psql -c """select cand_2gram.*, count 
	into cand_2gram_positive
	from cand_2gram, ngram_2_reduced
	where count > 1000 and feature_gram = gram;""" $DB_NAME

# TODO TUNE parameter A

# Distinct
psql -c """select candidate_id
	into cand_2gram_somepos_candidates
	from cand_2gram_positive, cand_word
	where cand_word_id = cand_word.id
	group by candidate_id;
	""" $DB_NAME


# # Distinct
# psql -c """select cand_word_id, 
# 	max(count) as count, max(candidate_id) as candidate_id
# 	into cand_2gram_map_pos
# 	from cand_2gram_positive, cand_word
# 	where cand_word_id = cand_word.id
# 	group by cand_word_id;
# 	""" $DB_NAME


# # FEATURE (HP POS): only if all words in a candidate appears in 2gram.
# # So mark all unselected candidate_ids...

# psql -c """select cand_word.candidate_id
# 	into cand_2gram_somepos_candidates
# 	from cand_word, cand_2gram_map_pos 
# 	where cand_word.id = cand_word_id 
# 	group by cand_word.candidate_id;
# 	""" $DB_NAME


# psql -c """select candidate_id 
# 	into cand_2gram_allneg_candidates
# 	from cand_word 
# 	where not exists 
# 	(select * from cand_2gram_map_pos
# 		where cand_word.id = cand_word_id)
# 	group by candidate_id""" $DB_NAME



########## 

# # Negative distinct map
# psql -c """select id as cand_word_id, candidate_id
# 	into cand_2gram_map_neg
# 	from cand_word
# 	where not exists 
# 	(select * from cand_2gram_map_pos 
# 		where cand_2gram_map_pos.cand_word_id = cand_word.id)""" $DB_NAME


# TODO TUNE parameter B (now fixed equal to 1000)

# FEATURE (HP NEG): only if all words in a candidate appears in 2gram.
# So mark all unselected candidate_ids...

psql -c """select candidate_id
	into cand_2gram_someneg_candidates
	from cand_word
	where not exists 
	(select * from cand_2gram_positive
		where cand_word_id = cand_word.id)
	group by candidate_id;""" $DB_NAME



# psql -c """select candidate_id 
# 	into cand_2gram_allpos_candidates
# 	from cand_word 
# 	where not exists
# 	(select * from cand_2gram_map_neg
# 		where cand_word.id = cand_word_id)
# 	group by candidate_id""" $DB_NAME
