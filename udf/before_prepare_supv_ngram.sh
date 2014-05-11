psql -c """drop table if exists supv_ngram cascade;
""" $DB_NAME

psql -c """create table supv_ngram(
  docid TEXT,
  ngram TEXT
  ) DISTRIBUTED BY (docid);
""" $DB_NAME
