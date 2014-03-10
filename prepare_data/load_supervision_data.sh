DB_NAME=ddocr
# SUPV_DIR=../data/test-supervision
SUPV_DIR=`cd $(dirname $0)/../data/test-supervision; pwd`

psql -c "DROP TABLE IF EXISTS html_1gram CASCADE;" $DB_NAME
psql -c "DROP TABLE IF EXISTS html_2gram CASCADE;" $DB_NAME
psql -c "DROP TABLE IF EXISTS html_3gram CASCADE;" $DB_NAME

psql -c "create table html_1gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, freq INT);" $DB_NAME

psql -c "create table html_2gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, word2 TEXT, freq INT); " $DB_NAME

psql -c "create table html_3gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, word2 TEXT, word3 TEXT, freq INT); " $DB_NAME

sed 's/\\/\\\\/g' $SUPV_DIR/*.1gram | psql -c "COPY html_1gram(docid, freq, word1) FROM STDIN;" $DB_NAME
  
sed 's/\\/\\\\/g' $SUPV_DIR/*.2gram | psql -c "COPY html_2gram(docid, freq, word1, word2) FROM STDIN;" $DB_NAME

sed 's/\\/\\\\/g' $SUPV_DIR/*.3gram | psql -c "COPY html_3gram(docid, freq, word1, word2, word3) FROM STDIN;" $DB_NAME
  