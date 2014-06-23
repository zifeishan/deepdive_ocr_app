#! /usr/bin/env bash

# psql -c """create table cand_2gram(id BIGSERIAL PRIMARY KEY, 
#   cand_word_id BIGSERIAL,
#   ngram TEXT);""" $DBNAME

psql -c "drop table if exists cand_2gram_positive cascade;" $DBNAME
psql -c "drop table if exists cand_2gram_somepos_candidates cascade;" $DBNAME
psql -c "drop table if exists cand_2gram_someneg_candidates cascade;" $DBNAME

psql -c """
	CREATE TABLE cand_2gram_positive AS 
		select cand_2gram.*, count 
		from cand_2gram, ngram_2_reduced
	where count > 1000 and ngram = gram
	-- DISTRIBUTED BY (docid);
	""" $DBNAME

# TODO TUNE parameter A

# Distinct
psql -c """
CREATE TABLE cand_2gram_somepos_candidates AS
	select 	cand_word.docid, 
					cand_word.candidate_id
	from 	cand_2gram_positive t,
				cand_word
	where cand_word.cand_word_id = t.cand_word_id
	  AND cand_word.docid = t.docid
	group by cand_word.docid, cand_word.candidate_id
	-- DISTRIBUTED BY (docid);
	""" $DBNAME


# # Distinct
# psql -c """select cand_word_id, 
# 	max(count) as count, max(candidate_id) as candidate_id
# 	into cand_2gram_map_pos
# 	from cand_2gram_positive, cand_word
# 	where cand_word_id = cand_word.id
# 	group by cand_word_id;
# 	""" $DBNAME


# # FEATURE (HP POS): only if all words in a candidate appears in 2gram.
# # So mark all unselected candidate_ids...

# psql -c """select cand_word.candidate_id
# 	into cand_2gram_somepos_candidates
# 	from cand_word, cand_2gram_map_pos 
# 	where cand_word.id = cand_word_id 
# 	group by cand_word.candidate_id;
# 	""" $DBNAME


# psql -c """select candidate_id 
# 	into cand_2gram_allneg_candidates
# 	from cand_word 
# 	where not exists 
# 	(select * from cand_2gram_map_pos
# 		where cand_word.id = cand_word_id)
# 	group by candidate_id""" $DBNAME



########## 

# # Negative distinct map
# psql -c """select id as cand_word_id, candidate_id
# 	into cand_2gram_map_neg
# 	from cand_word
# 	where not exists 
# 	(select * from cand_2gram_map_pos 
# 		where cand_2gram_map_pos.cand_word_id = cand_word.id)""" $DBNAME


# TODO TUNE parameter B (now fixed equal to 1000)

# FEATURE (HP NEG): only if all words in a candidate appears in 2gram.
# So mark all unselected candidate_ids...

psql -c """
CREATE TABLE cand_2gram_someneg_candidates AS 
	SELECT cand_word.docid, cand_word.candidate_id
	FROM   cand_word
	WHERE NOT EXISTS 
	(	select * 
		from 	cand_2gram_positive t
		where t.cand_word_id = cand_word.cand_word_id
		and   t.docid 			 = cand_word.docid
	)
	group by cand_word.docid, cand_word.candidate_id
-- DISTRIBUTED BY (docid);
""" $DBNAME



# psql -c """select candidate_id 
# 	into cand_2gram_allpos_candidates
# 	from cand_word 
# 	where not exists
# 	(select * from cand_2gram_map_neg
# 		where cand_word.id = cand_word_id)
# 	group by candidate_id""" $DBNAME
