#! /usr/bin/env bash

# psql -c "DROP TABLE IF EXISTS cand_label CASCADE;" ddocr

# # Exact same lables with candidate
# psql -c """create table cand_label(id BIGSERIAL PRIMARY KEY, 
#   candidate_id BIGSERIAL REFERENCES candidate(id),
#   label BOOLEAN);""" ddocr

psql -c "update candidate set label = NULL;" ddocr
echo "Evaluation document set:"
psql -c """select * from document;""" ddocr
