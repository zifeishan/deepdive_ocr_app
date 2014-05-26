DBNAME=$2

if [ $# != 3 ]; then
  echo "Usage: $0 tsv_path DBNAME table_name"
  exit
fi

psql -c "
  DROP TABLE IF EXISTS $3 CASCADE;
  
  CREATE TABLE $3(
    gram text,
    count real
    ) DISTRIBUTED BY (gram);
" $DBNAME

psql -c "
DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);
" $DBNAME

psql -c "
COPY $3 FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;;
" $DBNAME < $1

psql -c "
ANALYZE $3;
" $DBNAME
