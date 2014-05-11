#! /usr/bin/env bash
psql -c "DROP TABLE IF EXISTS feature CASCADE;" $DB_NAME

# # MUST drop in this case since ID can start from 1...
# psql -c """create table feature(id BIGSERIAL PRIMARY KEY, 
#   candidateid BIGSERIAL REFERENCES candidate(id),
#   fname TEXT,
#   fval BOOLEAN);""" $DB_NAME

psql -c """create table feature(
  docid         TEXT,
  cand_word_id  BIGINT,
  fname         TEXT,
  fval          BOOLEAN
  ) DISTRIBUTED BY(docid);
""" $DB_NAME
