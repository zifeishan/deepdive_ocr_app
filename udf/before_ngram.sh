#! /usr/bin/env bash
psql -c "DROP TABLE IF EXISTS f_$1gram CASCADE;" $DBNAME

psql -c """
  CREATE TABLE f_$1gram (
    docid TEXT,
    candidate_id TEXT,
    ngram text,
    count int)
DISTRIBUTED BY (docid);
""" $DBNAME