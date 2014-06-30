set -e


if [ $# != 2 ]; then
  echo "Usage: $0 tsv_path DBNAME"
  exit
fi

export DBNAME=$2
export TSV_PATH=$1

psql -c "

  DROP TABLE IF EXISTS tmp_entity_kb CASCADE;
  
  CREATE TABLE tmp_entity_kb (
    name text,
    class text,
    subclass text
    );
  
" $DBNAME

# for sed
TAB=$'\t'

##### Copy interval
# Sample data:
# ==> /dfs/hulk/0/zifei/ocr/kb/intervals.tsv <==
# 174.1000        170.3000        Aalenian
# 466.0000        460.9000        Abereiddian
# 513.0000        501.0000        Acadian
cut -f 3 $TSV_PATH/intervals.tsv | sed 's/$/'"${TAB}"'INTERVAL'"${TAB}"'interval/g' | psql -c "
COPY tmp_entity_kb(name, class, subclass) FROM STDIN (ERROR_LOGGING, ERROR_LOGGING_SKIP_BAD_ROWS);
" $DBNAME

##### Copy taxons
# Sample data:
# ==> /dfs/hulk/0/zifei/ocr/kb/paleodb_taxons.tsv <==
# Agaricocrinites genus
# Eukaryota       kingdom
# Metazoa subkingdom
# Actinopoda      phylum
cat $TSV_PATH/paleodb_taxons.tsv | sed 's/$/'"${TAB}"'TAXON/g' | psql -c "
COPY tmp_entity_kb(name, subclass, class) FROM STDIN (ERROR_LOGGING, ERROR_LOGGING_SKIP_BAD_ROWS);
" $DBNAME

psql -c "
ANALYZE tmp_entity_kb;
" $DBNAME

psql -c "
DROP TABLE IF EXISTS entity_kb CASCADE;

CREATE TABLE entity_kb AS
SELECT DISTINCT name, class, subclass
FROM tmp_entity_kb
;

" $DBNAME

