#! /usr/bin/env bash
psql -c """update cand_label
  set label = true
  where id in 
  (select cand_label.id from (cand_label natural join candidate) join html_1gram 
          on candidate.docid = html_1gram.docid and word = word1);
""" ddocr

psql -c """update cand_label
  set label = false
  where label is null 
  and id in 
  (select cand_label.id from (cand_label natural join candidate) join html_1gram 
          on candidate.docid = html_1gram.docid);  -- have supervision data
""" ddocr