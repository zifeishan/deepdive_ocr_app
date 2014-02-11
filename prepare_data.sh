#! /bin/bash

# Configuration
DB_NAME=deepdive_ocr

cd `dirname $0`
BASE_DIR=`pwd`

# dropdb $DB_NAME
# createdb $DB_NAME

# psql -c "drop schema if exists public cascade; create schema public;" $DB_NAME

psql -c "drop table features, feature_names, label1, label2, labelC, labelT CASCADE;" $DB_NAME

psql -c "create table features(id bigserial primary key, word_id int, feature_id int, feature_val boolean);" $DB_NAME
# psql -c "insert into people(id, name) values(6, 'Helen');" $DB_NAME

psql -c "create table feature_names(fid int primary key, fname varchar(20));" $DB_NAME
psql -c "create table labelT(id bigserial primary key, wid int, val boolean);" $DB_NAME
psql -c "create table labelC(id bigserial primary key, wid int, val boolean);" $DB_NAME

psql -c "COPY features(word_id, feature_id, feature_val) FROM '$BASE_DIR/data/raw/feature_table.csv' DELIMITER ',' CSV;" $DB_NAME
psql -c "COPY labelT(wid, val) FROM '$BASE_DIR/data/raw/labelT_table.csv' DELIMITER ',' CSV;" $DB_NAME
psql -c "COPY labelC(wid, val) FROM '$BASE_DIR/data/raw/labelC_table.csv' DELIMITER ',' CSV;" $DB_NAME