psql -c """drop table if exists tmp_domain_$1gram cascade;
""" $DB_NAME

psql -c """create table tmp_domain_$1gram(
  doc_id BIGINT,
  ngram TEXT,
  count REAL
  ) DISTRIBUTED BY (doc_id);
""" $DB_NAME
