#! /usr/bin/env bash

psql -c "DROP TABLE IF EXISTS cand_2gram CASCADE;" $DB_NAME

psql -c """create table cand_2gram(id BIGSERIAL PRIMARY KEY, 
  cand_word_id BIGSERIAL,
  feature_gram TEXT);""" $DB_NAME
