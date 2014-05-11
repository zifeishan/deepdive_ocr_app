#! /usr/bin/env bash

# psql -c "DROP TABLE IF EXISTS cand_label CASCADE;" $DB_NAME

# # Exact same lables with candidate
# psql -c """create table cand_label(id BIGSERIAL PRIMARY KEY, 
#   candidate_id BIGSERIAL REFERENCES candidate(id),
#   label BOOLEAN);""" $DB_NAME

psql -c "update candidate set label = NULL;" $DB_NAME
echo "Evaluation document set:"
psql -c """select * from document;""" $DB_NAME
