#! /bin/bash

# Configuration
# export DB_NAME=ddocr
# export DB_NAME=ddocr_large
export DB_NAME=$1
echo "DBNAME is $1"
# PGPORT=${PGPORT:5432}

APP_HOME=`cd $(dirname $0)/..; pwd`
echo $APP_HOME

# CAND_DIR=$APP_HOME/data/journals-test-output2-new
# CAND_DIR=$APP_HOME/data/journal-test-output3-distinct
# CAND_DIR=/dfs/madmax/0/zifei/deepdive/app/ocr/data/journals-output
CAND_DIR=/lfs/local/0/zifei/deepdive/app/ocr/data/journals-output-new


## Do not discard previous db: load ngram data takes time..
# dropdb $DB_NAME
# createdb $DB_NAME
# psql -c "drop schema if exists public cascade; create schema public;" $DB_NAME

# Create error table
psql -c """DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);""" $DB_NAME

# READ cand_word table from data
psql -c "drop table if exists cand_word CASCADE;" $DB_NAME
psql -c """create table cand_word(
  id BIGSERIAL,
  candidate_id BIGINT,
  docid TEXT,
  varid INT, -- start from 1
  candid INT, -- start from 0, multinomial, according to source
  source TEXT, -- 1-1 mapping to source
  wordid INT, -- start from 0
  word TEXT,
  page INT, 
  l INT, 
  t INT, 
  r INT, 
  b INT,  
  pos TEXT,
  ner TEXT,
  stem TEXT)
DISTRIBUTED BY (docid);""" $DB_NAME

# sed 's/\\/\\\\/g' $CAND_DIR/*.cand_word | psql -c "COPY cand_word(docid, varid, candid, source, wordid, word, page, l, t, r, b, pos, ner, stem) FROM STDIN;" $DB_NAME
sed 's/\\/\\\\/g' $CAND_DIR/JOURNAL_*.cand_word | psql -c "COPY cand_word(docid, varid, candid, source, wordid, word, page, l, t, r, b, pos, ner, stem) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000000000 ROWS;" $DB_NAME

# Variable table
psql -c "drop table if exists variable cascade;" $DB_NAME
psql -c """create table variable(
  id BIGSERIAL, 
  docid TEXT,
  varid INT,
  label INT)
DISTRIBUTED BY (docid);
""" $DB_NAME

psql -c """insert into variable(docid, varid) select distinct docid, varid from cand_word order by docid, varid;""" $DB_NAME

# Candidate table
psql -c "drop table if exists candidate cascade;" $DB_NAME
psql -c """create table candidate(
  id BIGSERIAL, 
  variable_id BIGINT,
  docid TEXT,
  varid INT,  -- redundancy
  candid INT,
  source TEXT,
  label BOOLEAN)
DISTRIBUTED BY (docid);
""" $DB_NAME
psql -c """insert into candidate(variable_id, docid, varid, candid, source) 
  select distinct variable.id as variable_id, variable.docid, variable.varid, candid, source
  from cand_word, variable 
    where variable.docid = cand_word.docid
      and variable.varid = cand_word.varid
  order by variable_id, candid, source;
  """ $DB_NAME

# Update cand_word
psql -c """update cand_word 
  set candidate_id = candidate.id
  from candidate
  where cand_word.docid = candidate.docid
    and cand_word.varid = candidate.varid
    and cand_word.candid = candidate.candid
  ;
""" $DB_NAME




################ PREVIOUS DESIGN ###############

# # prevent '\' crashing COPY.
# sed 's/\\/\\\\/g' $CAND_DIR/*.cand | psql -c "COPY candidate_with_word(docid, wordid, candid_tot, source, word) FROM STDIN;" $DB_NAME

# cat $CAND_DIR/*.candbox | psql -c "COPY cand_box(docid, wordid, candid, page, l, t, r, b) FROM STDIN;" $DB_NAME
  
# sed 's/\\/\\\\/g' $CAND_DIR/*.candfeature | psql -c "COPY cand_feature(docid, wordid, candid, pos, ner, stem) FROM STDIN;" $DB_NAME
#   