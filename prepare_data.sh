#! /bin/bash

# Configuration
DB_NAME=ddocr
DB_PORT=5432

cd `dirname $0`
BASE_DIR=`pwd`

# dropdb $DB_NAME
# createdb $DB_NAME
# psql -p $DB_PORT -c "drop schema if exists public cascade; create schema public;" $DB_NAME

# psql -p $DB_PORT -c "drop table labels, features, feature_names, actual_words, options CASCADE;" $DB_NAME
psql -p $DB_PORT -c "drop table factor_variables, factors, inference_result, inference_result_weights, variables, weights cascade;" $DB_NAME


psql -p $DB_PORT -c "drop table features, feature_names, labels, actual_words, options CASCADE;" $DB_NAME

psql -p $DB_PORT -c "create table features(id BIGSERIAL PRIMARY KEY, docid TEXT, wordid INT, feature_name TEXT, feature_val BOOLEAN);" $DB_NAME

psql -p $DB_PORT -c "create table labels(id bigserial primary key, docid TEXT, wordid INT, label_t BOOLEAN, label_c BOOLEAN);" $DB_NAME

psql -p $DB_PORT -c "create table actual_words(id bigserial primary key, docid TEXT, wordid INT, word TEXT);" $DB_NAME

psql -p $DB_PORT -c "create table options(id bigserial primary key, docid TEXT, wordid INT, option_t TEXT, option_c TEXT);" $DB_NAME

# psql -p $DB_PORT -c "create table feature_names(id bigserial primary key, feature_name TEXT);" $DB_NAME


cat data/processed-tables/*.features.txt | psql -p $DB_PORT -c "COPY features(docid, wordid, feature_name, feature_val) FROM STDIN" $DB_NAME

cat data/processed-tables/*.labels.txt | psql -p $DB_PORT -c "COPY labels(docid, wordid, label_t, label_c) FROM STDIN" $DB_NAME

cat data/processed-tables/*.corrected_words.txt | psql -p $DB_PORT -c "COPY actual_words(docid, wordid, word) FROM STDIN" $DB_NAME

cat data/processed-tables/*.options.txt | psql -p $DB_PORT -c "COPY options(docid, wordid, option_t, option_c) FROM STDIN" $DB_NAME

# cat data/processed-tables/*.feature_names.txt | psql -p $DB_PORT -c "COPY feature_names(docid, feature_name) FROM STDIN" $DB_NAME
