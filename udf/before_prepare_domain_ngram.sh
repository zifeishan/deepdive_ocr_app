psql -c """drop table if exists doc_domain_$1gram cascade;
""" $DB_NAME

psql -c """create table doc_domain_$1gram(
  docid TEXT,
  ngram TEXT,
  count REAL
  ) DISTRIBUTED BY (docid);
""" $DB_NAME
