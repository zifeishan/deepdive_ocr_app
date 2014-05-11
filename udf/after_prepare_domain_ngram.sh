psql -c "drop table if exists domain_$1gram cascade;
" $DB_NAME

psql -c "
  CREATE TABLE domain_$1gram AS 
  SELECT   ngram, sum(count) as count
  FROM     tmp_domain_$1gram
  WHERE    count >= $2
  GROUP BY ngram
  DISTRIBUTED BY (ngram);
" $DB_NAME

# psql -c "
#   DROP TABLE tmp_domain_$1gram CASCADE;
# " $DB_NAME