#! /usr/bin/env bash

# If any (all) word is true, label its (father) candidate as true
psql -c """update candidate
  set label = true
  where id in 
  (select candidate_id from cand_word 
    where (docid, word) in 
    (select docid, word1 from html_1gram)
    );
""" $DB_NAME

# If one word is false, label candidate as false
# # AVOID NOT IN, SLOW!!
psql -c """update candidate
  set label = false
  where id in 
  (select distinct candidate_id from cand_word 
    where not exists 
    (select docid, word1 from html_1gram 
      where docid = cand_word.docid 
        and word1 = word)
    );
""" $DB_NAME

# Break ties with "unknown"...
#### But allow multiple SAME words to be true
# Do not allow multiple SAME words to be true! Distinct candidates!
psql -c """update candidate
  set label = null
  where id in (
    select c1.id
    from candidate as c1 join candidate as c2 
    on c1.variable_id = c2.variable_id
    -- and c1.word != c2.word
    and c1.id != c2.id
    and c1.label = true
    and c2.label = true);
""" $DB_NAME



############### 2gram supervision for BREAK TIES ########

# Create view for 2gram supervision
# two continuous cand_words
psql -c """create view html_2gram_supv_result as (
  select c1.id as \"c1.id\", c2.id as \"c2.id\", c1.docid, c1.wordid, c1.word as \"c1.word\", c2.word as \"c2.word\", html_2gram.freq
from cand_word as c1, cand_word as c2, html_2gram, candidate
where label is null
TODO!!!!!!!!!!!!!
and c1.docid = c2.docid
and c1.docid = html_2gram.docid
and c1.wordid = c2.wordid - 1
and c1.word = word1
and c2.word = word2
);
""" $DB_NAME

# 2gram supervision

psql -c """drop table if exists toupdate;
select distinct \"c1.id\" as id into toupdate from html_2gram_supv_result;
insert into toupdate (select distinct \"c2.id\" as id from html_2gram_supv_result);""" $DB_NAME

psql -c """update cand_label
  set label = true
  where candidateid in (select * from toupdate);""" $DB_NAME

# Break ties with "unknown"...
# But allow multiple SAME words to be true
psql -c """update cand_label
  set label = null
  where candidateid in (
    select c1.id
    from cand_with_label as c1 join cand_with_label as c2 
    on c1.docid = c2.docid and c1.wordid = c2.wordid 
    and c1.word != c2.word
    and c1.label = true
    and c2.label = true);
""" $DB_NAME



# #############################
# # HOLD OUT
# psql -c """update cand_label 
#   set label = null 
#   where candidateid in (
#     select id from candidate where docid in (select docid from eval_docs));""" $DB_NAME
