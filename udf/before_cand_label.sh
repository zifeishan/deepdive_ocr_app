#! /usr/bin/env bash
psql -c "DROP TABLE IF EXISTS cand_label CASCADE;" ddocr

# Exact same lables with candidate
psql -c """create table cand_label(id BIGSERIAL PRIMARY KEY, 
  label BOOLEAN);""" ddocr
