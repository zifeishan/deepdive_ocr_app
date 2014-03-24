#! /usr/bin/env bash

# psql -c """create view cand_with_label as select label, candidate.* from cand_label right join candidate on cand_label.candidateid = candidate.id;""" ddocr

## NOTE: This step is redundant
# # If any (all) word is true, label its (father) candidate as true
# psql -c """update candidate
#   set label = true
#   where id in 
#   (select candidate_id from cand_word 
#     where (docid, word) in 
#     (select docid, word1 from html_1gram)
#     );
# """ ddocr

# If one word is false, label candidate as false

 
# # AVOID NOT IN, SLOW!!
# psql -c """update candidate
#   set label = false
#   where id in 
#   (select distinct candidate_id from cand_word 
#     where (docid, word) not in (select docid, word1 from html_1gram)
#   );
# """ ddocr

psql -c """update candidate
  set label = false
  where id in 
  (select distinct candidate_id from cand_word 
    where not exists 
    (select docid, word1 from html_1gram 
      where docid = cand_word.docid 
        and word1 = word)
    );
  update candidate set label = true where label is null;
""" ddocr

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
""" ddocr



#############################
# HOLD OUT
psql -c """update candidate 
  set label = null 
  where docid in (select docid from eval_docs);""" ddocr
