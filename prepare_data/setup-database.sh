#! /bin/bash
set -e

if hash psql 2>/dev/null; then  # check psql exists
    true
else
    echo 'ERROR: psql does not exist.'
    exit
fi

if [ $# = 2 ]; then          # Export DBNAME from command line
  export DBNAME=$1
  export DOCLIST=$2
else
  echo 'Usage: '$0' DBNAME DOCLIST'
  echo 'e.g. '$0' ddocr_100 ../data/doclist/doclist-1k.txt'
  exit
fi

# CAND_DIR=/dfs/hulk/0/zifei/ocr/journals-output/
# SUPV_DIR=/dfs/hulk/0/zifei/ocr/supervision_escaped/
# GOOGLE_1GRAM_TSV=/dfs/hulk/0/zifei/ocr/google-ngram/1gram.tsv
# GOOGLE_2GRAM_TSV=/dfs/hulk/0/zifei/ocr/google-ngram/2gram_reduced.tsv
# DOMAIN_CORPUS=/dfs/hulk/0/zifei/ocr/domain-corpus.tsv
echo "Data dir:
CAND_DIR: $CAND_DIR
SUPV_DIR: $SUPV_DIR
GOOGLE_1GRAM_TSV: $GOOGLE_1GRAM_TSV
GOOGLE_2GRAM_TSV: $GOOGLE_2GRAM_TSV
"

echo "Creating database..."
createdb $DBNAME
if [ "$?" != "0" ]; then echo "[00] FAILED! Database already exists."; exit 1; fi

echo "loading aligned OCR outputs..."
pypy load_aligned_ocr_outputs_from_list.py $DBNAME $CAND_DIR $DOCLIST
if [ "$?" != "0" ]; then echo "[10] FAILED!"; exit 1; fi

echo "loading supervision sequence..."
pypy load_supervision_seq_from_list.py $DBNAME $SUPV_DIR $DOCLIST
if [ "$?" != "0" ]; then echo "[20] FAILED!"; exit 1; fi

echo "Loading google 1gram..."
# pypy load_google_ngram.py /dfs/hulk/0/zifei/ocr/google-ngram/1gram/ ngram_1
bash load_google_ngram_from_dump.sh $GOOGLE_1GRAM_TSV $DBNAME google_1gram

if [ "$?" != "0" ]; then echo "[30] FAILED!"; exit 1; fi

echo "Loading google 2gram..."
bash load_google_ngram_from_dump.sh $GOOGLE_2GRAM_TSV $DBNAME google_2gram_reduced
if [ "$?" != "0" ]; then echo "[40] FAILED!"; exit 1; fi

echo "Loading domain corpus..."
# pypy load_domain_corpus.py $DBNAME $SUPV_DIR
psql -c "
  DROP TABLE IF EXISTS domain_corpus CASCADE;
  
  CREATE TABLE domain_corpus(
    docid text,
    article text
    ) DISTRIBUTED BY (docid);
" $DBNAME

psql -c "
DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);

COPY domain_corpus FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;;
" $DBNAME < $DOMAIN_CORPUS

psql -c "
ANALYZE domain_corpus;
" $DBNAME
if [ "$?" != "0" ]; then echo "[50] FAILED!"; exit 1; fi

cat /dfs/hulk/0/zifei/ocr/kb/entity_kb.tsv | psql -c "
DROP TABLE IF EXISTS entity_kb;
CREATE TABLE entity_kb (
    name text,
    class text,
    subclass text
);
COPY entity_kb FROM STDIN;" $DBNAME
if [ "$?" != "0" ]; then echo "[60] FAILED!"; exit 1; fi


echo "Done!"
echo "Remember to setup contrib module. e.g.: psql $DBNAME -f /usr/local/Cellar/postgresql/9.3.4/share/postgresql/contrib/fuzzystrmatch.sql (OR: /lfs/rambo/0/zifei/software/greenplum-db-4.2.2.4/share/postgresql/contrib/fuzzystrmatch.sql)"
