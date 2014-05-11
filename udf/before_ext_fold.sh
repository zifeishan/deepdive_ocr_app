#! /usr/bin/env bash
echo "Running script: BEFORE EXT FOLD"

# Document table
psql -c "drop table if exists document cascade;" $DB_NAME
psql -c "create table document(id bigserial primary key, docid text);" $DB_NAME
psql -c "insert into document(docid) select distinct docid from cand_word order by docid;" $DB_NAME

psql -c "drop table if exists document_backup cascade;" $DB_NAME
psql -c "select * into document_backup from document;" $DB_NAME

# HOLD OUT docs
psql -c """create view eval_docs as
select docid from document_backup where id in (select id from document where docid is null);
""" $DB_NAME
