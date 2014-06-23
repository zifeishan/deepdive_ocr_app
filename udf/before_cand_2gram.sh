#! /usr/bin/env bash

psql -c "DROP TABLE IF EXISTS cand_2gram CASCADE;" $DB_NAME

psql -c """create table cand_2gram(
  docid TEXT,
  cand_word_id BIGINT,
  feature_gram TEXT)
-- DISTRIBUTED BY (docid);""" $DB_NAME
