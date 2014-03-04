#! /usr/bin/env bash
echo "Running script: BEFORE EXT FOLD"
psql -c "drop table if exists document;" ddocr
psql -c "create table document(id bigserial primary key, docid text);" ddocr
psql -c "insert into document(docid) select distinct docid from candidate;" ddocr

psql -c "drop table if exists document_backup;" ddocr
psql -c "select * into document_backup from document;" ddocr
