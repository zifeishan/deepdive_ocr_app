#! /usr/bin/env bash

psql -c "

  UPDATE candidate 
  SET label = NULL;

  UPDATE  candidate
  SET     label = TRUE
  FROM    cand_$1gram cand,
          supv_ngram supv
  WHERE   candidate.docid = cand.docid
    AND   supv.docid = cand.docid
    AND   candidate.candidate_id = cand.candidate_id
    AND   cand.ngram = supv.ngram
    ;

" $DB_NAME
psql -c "

  UPDATE candidate 
  SET    label = FALSE
  WHERE  label IS NULL;

" $DB_NAME
psql -c "

  UPDATE candidate AS c1
  SET    label = null
  FROM   candidate AS c2
  WHERE  c1.docid = c2.docid
    AND  c1.variable_id = c2.variable_id
    AND  c1.candidate_id != c2.candidate_id
    AND  c1.label = true
    AND  c2.label = true;

" $DB_NAME

psql -c "ANALYZE candidate;" $DB_NAME
