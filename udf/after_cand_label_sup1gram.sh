#! /usr/bin/env bash

psql -c """create view cand_with_label as select label, candidate.* from cand_label right join candidate on cand_label.candidateid = candidate.id;""" ddocr

psql -c """update cand_label
  set label = true
  where candidateid in 
  (select candidate.id from candidate join html_1gram 
          on candidate.docid = html_1gram.docid and word = word1);
""" ddocr

# If some candidate in the word is true, others are false

psql -c """update cand_label
  set label = false
  where candidateid in (
    select c2.id 
    from cand_with_label as c1 join cand_with_label as c2 
    on c1.docid = c2.docid and c1.wordid = c2.wordid 
    and c1.candid != c2.candid and c1.word != c2.word  -- redundant
    and c1.label = true
    and c2.label is null);""" ddocr

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
""" ddocr



#############################
# HOLD OUT
psql -c """update cand_label 
  set label = null 
  where candidateid in (
    select id from candidate where docid in (select docid from eval_docs));""" ddocr
