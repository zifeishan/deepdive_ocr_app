#! /usr/bin/env bash

echo "Positive examples (rough):"
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
echo "Negative examples:"
psql -c "

  UPDATE candidate c1
  SET    label = FALSE
  WHERE   label IS NULL 
    AND   EXISTS (        -- UPDATE: treat not aligned guys as unknown
      SELECT * 
      FROM candidate c2
      WHERE c1.docid = c2.docid
      AND   c1.variable_id = c2.variable_id
      AND   c1.candidate_id != c2.candidate_id
      AND   c2.label = true
      );
" $DB_NAME
echo "Break ties:"
psql -c "        --- Treat duplicated guys as unknown

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

# Check
psql -c "
  SELECT source, label, count(*) FROM candidate
  GROUP BY source, label
  ORDER BY source, label;
" $DBNAME 