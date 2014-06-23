#! /usr/bin/env bash

psql -c "DROP TABLE IF EXISTS cand_$1gram CASCADE;" $DB_NAME

psql -c """create table cand_$1gram(
  docid         TEXT,
  cand_word_id  TEXT,
  candidate_id  TEXT,
  ngram         TEXT
  )
-- DISTRIBUTED BY (docid);""" $DB_NAME
