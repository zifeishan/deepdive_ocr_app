if [ $# = 1 ]; then
  export DBNAME=$1
else
  export DBNAME=ddocr_1k
fi
echo "Set DB_NAME to ${DBNAME}."

export EXPORT_ROOT='/tmp'

# export EVAL_DIR=/dfs/madmax5/0/zifei/deepdive/app/ocr/data/evaluation/
export EVAL_DIR=data/test-evaluation/

psql -c """copy (select docid, varid, word from cand_word 
  where (source = 'T' or source = 'CT' or source = 'TC')
  order by docid, varid, candid, wordid) to '$EXPORT_ROOT/ocr-output-words-tesseract-all.tsv'""" $DBNAME

psql -c """copy (select docid, varid, word from cand_word 
  where (source = 'C' or source = 'CT' or source = 'TC')
  order by docid, varid, candid, wordid) to '$EXPORT_ROOT/ocr-output-words-cuneiform-all.tsv';""" $DBNAME

scp rocky:/tmp/ocr-output-words-*-all.tsv /tmp/

pypy ocr-evaluation.py /tmp/ocr-output-words-tesseract-all.tsv $EVAL_DIR evaluation/bestpick-ocr-benchmark/tesseract/ evaluation/bestpick-ocr-benchmark/eval-results-tess-all.txt

pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform-all.tsv $EVAL_DIR evaluation/bestpick-ocr-benchmark/tesseract/ evaluation/bestpick-ocr-benchmark/eval-results-cuni-all.txt