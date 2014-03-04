#! /usr/bin/env bash
echo "Running script: BEFORE EXT FOLD"
psql -c "drop table if exists document cascade;" ddocr
psql -c "create table document(id bigserial primary key, docid text);" ddocr
psql -c "insert into document(docid) select distinct docid from candidate;" ddocr

psql -c "drop table if exists document_backup cascade;" ddocr
psql -c "select * into document_backup from document;" ddocr

# HOLD OUT docs
psql -c """create view eval_docs as
select docid from document_backup where id in (select id from document where docid is null);
""" ddocr
