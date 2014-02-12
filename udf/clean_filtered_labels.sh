#! /usr/bin/env bash
# psql -c "TRUNCATE filtered_labels CASCADE;" ddocr
psql -c "DROP TABLE IF EXISTS filtered_labels CASCADE;" ddocr
psql -c """create table filtered_labels(id bigserial primary key, 
  docid TEXT, 
  wordid INT, 
  label_t BOOLEAN, 
  label_c BOOLEAN);""" ddocr
