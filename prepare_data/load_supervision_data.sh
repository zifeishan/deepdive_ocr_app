echo 'DBNAME is $1'

DB_NAME=$1
# SUPV_DIR=../data/test-supervision
# SUPV_DIR=`cd $(dirname $0)/../data/test-supervision; pwd`
# SUPV_DIR=/dfs/madmax/0/zifei/deepdive/app/ocr/data/supervision/supervision-data
SUPV_DIR=/lfs/local/0/zifei/deepdive/app/ocr/data/supervision/supervision-data

psql -c "DROP TABLE IF EXISTS html_1gram CASCADE;" $DB_NAME
psql -c "DROP TABLE IF EXISTS html_2gram CASCADE;" $DB_NAME
psql -c "DROP TABLE IF EXISTS html_3gram CASCADE;" $DB_NAME

# Create error table
psql -c """DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);""" $DB_NAME

psql -c "create table html_1gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, freq INT);" $DB_NAME

psql -c "create table html_2gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, word2 TEXT, freq INT); " $DB_NAME

psql -c "create table html_3gram(id BIGSERIAL PRIMARY KEY, docid TEXT, word1 TEXT, word2 TEXT, word3 TEXT, freq INT); " $DB_NAME

for file in `find $SUPV_DIR -name "*.1gram"`; do 
	echo $file
  sed 's/\\/\\\\/g' $file | psql -c "COPY html_1gram(docid, freq, word1) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" $DB_NAME
done

for file in `find $SUPV_DIR -name "*.2gram"`; do 
	echo $file
	sed 's/\\/\\\\/g' $file | psql -c "COPY html_2gram(docid, freq, word1, word2) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" $DB_NAME
done

for file in `find $SUPV_DIR -name "*.3gram"`; do 
	echo $file
  sed 's/\\/\\\\/g' $file | psql -c "COPY html_3gram(docid, freq, word1, word2, word3) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" $DB_NAME
done

# sed 's/\\/\\\\/g' $SUPV_DIR/*.1gram | psql -c "COPY html_1gram(docid, freq, word1) FROM STDIN;" $DB_NAME
  
# sed 's/\\/\\\\/g' $SUPV_DIR/*.2gram | psql -c "COPY html_2gram(docid, freq, word1, word2) FROM STDIN;" $DB_NAME

# sed 's/\\/\\\\/g' $SUPV_DIR/*.3gram | psql -c "COPY html_3gram(docid, freq, word1, word2, word3) FROM STDIN;" $DB_NAME
