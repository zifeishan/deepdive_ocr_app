#! /usr/bin/env bash

############### 2gram supervision ALONE (can also used for breaking ties) ########

# Create view for 2gram supervision
# two continuous cand_words
# TODO: Consider words across variables!!

psql -c """drop view if exists html_2gram_supv_incand, html_2gram_supv_crosscand cascade;""" ddocr 

psql -c "drop table if exists candidate_max_wordid cascade;" ddocr
# Inside candidate
psql -c """create view html_2gram_supv_incand as (
  select c1.id as c1id, c2.id as c2id, c1.candidate_id, c1.docid, c1.varid, c1.word as c1word, c2.word as c2word
from cand_word as c1, cand_word as c2, candidate
where candidate.label is null
-- and c1.docid = html_2gram.docid
and candidate.id = c1.candidate_id
and c1.candidate_id = c2.candidate_id
and c1.wordid = c2.wordid - 1
and not exists 
  (select * from html_2gram where 
  c1.docid = html_2gram.docid
  and c1.word = word1
  and c2.word = word2)
);
""" ddocr

psql -c """select candidate_id, max(wordid) as max_wordid
  into candidate_max_wordid
  from cand_word 
  group by candidate_id;""" ddocr

# Cross candidates
# c1: wordid last, varid (x-1)
# c2: wordid 0, varid (x)
psql -c """create view html_2gram_supv_crosscand as (
select c1.id as c1id, c2.id as c2id, c1.candidate_id as c1_cand_id, c2.candidate_id as c2_cand_id,
  c1.docid, c1.varid as c1_varid, c2.varid as c2_varid, c1.word as c1word, c2.word as c2word
  -- , html_2gram.freq
from cand_word as c1, cand_word as c2, 
  candidate as cd1, candidate as cd2, 
  -- html_2gram, 
  candidate_max_wordid
where cd1.label is null
and cd2.label is null
-- and c1.docid = html_2gram.docid
-- and c2.docid = html_2gram.docid
and c1.candidate_id = cd1.id
and c2.candidate_id = cd2.id
and c1.docid = c2.docid
and c1.varid = c2.varid - 1
and c2.wordid = 0
and c1.candidate_id = candidate_max_wordid.candidate_id
and not exists 
  (select * from html_2gram where 
  c1.docid = html_2gram.docid
  and c1.word = word1
  and c2.word = word2)
);
""" ddocr


# 2gram supervision

# Negative examples
psql -c """drop table if exists toupdate;
select distinct candidate_id into toupdate from html_2gram_supv_incand;
insert into toupdate (select distinct c1_cand_id as candidate_id from html_2gram_supv_crosscand);
insert into toupdate (select distinct c2_cand_id as candidate_id from html_2gram_supv_crosscand);
  """ ddocr

psql -c """update candidate
  set label = false
  where id in (select * from toupdate);""" ddocr

# Positive: others
psql -c """update candidate set label = true where label is null;""" ddocr

# Break ties with "unknown"...
# But allow multiple SAME words to be true
psql -c """update candidate
  set label = null
  where id in (
    select c1.id
    from candidate as c1 join candidate as c2 
    on c1.variable_id = c2.variable_id
    and c1.id != c2.id
    and c1.label = true
    and c2.label = true);
""" ddocr



#############################
# HOLD OUT
psql -c """update cand_label 
  set label = null 
  where candidateid in (
    select id from candidate where docid in (select docid from eval_docs));""" ddocr
