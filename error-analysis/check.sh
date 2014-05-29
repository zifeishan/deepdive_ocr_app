if hash psql 2>/dev/null; then  # check psql exists
    true
else
    echo 'ERROR: psql does not exist.'
    exit
fi

DOCID='JOURNAL_13504'
if [ $# = 1 ]; then
  export DOCID=$1
fi


grep $DOCID /tmp/ocr-output-words.tsv | cut -f 3 > tmp-dd-output.tsv
vimdiff tmp-dd-output.tsv /dfs/hulk/0/zifei/ocr/evaluation_escaped/JOURNAL_13504.seq
