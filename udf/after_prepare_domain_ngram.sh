psql -c "DROP TABLE IF EXISTS domain_$1gram CASCADE;
" $DB_NAME

psql -c "
  CREATE TABLE domain_$1gram AS 
  SELECT   ngram, sum(count) as count
  FROM     tmp_domain_$1gram
  WHERE    count >= $2
    AND    NOT EXISTS (
           SELECT * 
           FROM eval_docs 
           WHERE eval_docs.docid = tmp_domain_$1gram.docid
  ) GROUP BY ngram
  DISTRIBUTED BY (ngram);
" $DB_NAME

# psql -c "
#   DROP TABLE tmp_domain_$1gram CASCADE;
# " $DB_NAME
