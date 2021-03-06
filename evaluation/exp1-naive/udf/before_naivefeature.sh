#! /usr/bin/env bash
psql -c "DROP TABLE IF EXISTS feature CASCADE;" ddocr

# MUST drop in this case since ID can start from 1...
psql -c """create table feature(id BIGSERIAL PRIMARY KEY, 
  candidateid BIGSERIAL REFERENCES candidate(id),
  fname TEXT,
  fval BOOLEAN);""" ddocr
