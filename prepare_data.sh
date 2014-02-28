#! /bin/bash

# Configuration
DB_NAME=ddocr
PGPORT=${PGPORT:5432}

cd `dirname $0`
BASE_DIR=`pwd`

## Do not discard previous db: load ngram data takes time..
# dropdb $DB_NAME
# createdb $DB_NAME
# psql -c "drop schema if exists public cascade; create schema public;" $DB_NAME

# psql -c "drop table labels, features, feature_names, actual_words, options CASCADE;" $DB_NAME
psql -c "drop table factor_variables CASCADE;" $DB_NAME
psql -c "drop table factors CASCADE;" $DB_NAME
psql -c "drop table inference_result CASCADE;" $DB_NAME
psql -c "drop table inference_result_weights CASCADE;" $DB_NAME
psql -c "drop table variables CASCADE;" $DB_NAME
psql -c "drop table weights cascade;" $DB_NAME
psql -c "drop table features CASCADE;" $DB_NAME 
psql -c "drop table feature_names CASCADE;" $DB_NAME 
psql -c "drop table labels CASCADE;" $DB_NAME 
psql -c "drop table actual_words CASCADE;" $DB_NAME 
psql -c "drop table options CASCADE;" $DB_NAME

psql -c "drop table candidate CASCADE;" $DB_NAME
psql -c "drop table cand_box CASCADE;" $DB_NAME
psql -c "drop table cand_feature CASCADE;" $DB_NAME

psql -c "create table candidate(id BIGSERIAL PRIMARY KEY, docid TEXT, wordid INT, candid INT, source TEXT, word TEXT);" $DB_NAME

psql -c "create table cand_box(id BIGSERIAL PRIMARY KEY, docid TEXT, wordid INT, candid INT, page INT, l INT, t INT, r INT, b INT);" $DB_NAME
  
psql -c "create table cand_feature(id BIGSERIAL PRIMARY KEY, docid TEXT, wordid INT, candid INT, pos TEXT, ner TEXT, stem TEXT);" $DB_NAME
  

# psql -c "create table features(id BIGSERIAL PRIMARY KEY, docid TEXT, wordid INT, feature_name TEXT, feature_val BOOLEAN);" $DB_NAME

# psql -c "create table labels(id bigserial primary key, docid TEXT, wordid INT, label_t BOOLEAN, label_c BOOLEAN);" $DB_NAME

# psql -c "create table actual_words(id bigserial primary key, docid TEXT, wordid INT, word TEXT);" $DB_NAME

# psql -c "create table options(id bigserial primary key, docid TEXT, wordid INT, option_t TEXT, option_c TEXT);" $DB_NAME

# psql -c "create table feature_names(id bigserial primary key, feature_name TEXT);" $DB_NAME

# prevent '\' crashing COPY.
sed 's/\\/\\\\/g' data/journals-test-output/*.cand | psql -c "COPY candidate(docid, wordid, candid, source, word) FROM STDIN;" $DB_NAME

cat data/journals-test-output/*.candbox | psql -c "COPY cand_box(docid, wordid, candid, page, l, t, r, b) FROM STDIN;" $DB_NAME
  
sed 's/\\/\\\\/g' data/journals-test-output/*.candfeature | psql -c "COPY cand_feature(docid, wordid, candid, pos, ner, stem) FROM STDIN;" $DB_NAME
  


# cat data/processed-tables/*.features.txt | psql -c "COPY features(docid, wordid, feature_name, feature_val) FROM STDIN;" $DB_NAME

# cat data/processed-tables/*.labels.txt | psql -c "COPY labels(docid, wordid, label_t, label_c) FROM STDIN;" $DB_NAME

# cat data/processed-tables/*.corrected_words.txt | psql -c "COPY actual_words(docid, wordid, word) FROM STDIN;" $DB_NAME

# cat data/processed-tables/*.options.txt | psql -c "COPY options(docid, wordid, option_t, option_c) FROM STDIN;" $DB_NAME

# cat data/processed-tables/*.features.txt | psql -c "COPY features(docid, wordid, feature_name, feature_val) FROM STDIN;" $DB_NAME
