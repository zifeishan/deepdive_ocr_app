if [ "$#" -ne 1 ]; then
    echo "Usage: ... <dbname>. (uses PGHOST)"
else
  DBNAME=$1
fi
bash generate_ocr_result.sh $DBNAME
scp $PGHOST:/tmp/ocr-output* /tmp/
### pypy ocr-evaluation.py
# EVAL_DIR=/dfs/madmax5/0/zifei/deepdive/app/ocr/data/evaluation/
# EVAL_DIR=/dfs/madmax/0/zifei/deepdive/app/ocr/data/evaluation/
# EVAL_DIR=data/test-evaluation

rm -f eval-results/deepdive/*

export MAXPARALLEL=25
export EVAL_LIST_FILE=/tmp/ocr-eval-docs.tsv
export EVAL_DIR=/dfs/hulk/0/zifei/ocr/evaluation_escaped/
# pypy ocr-evaluation-strict.py /tmp/ocr-output-words.tsv $EVAL_DIR eval-results.txt

cat $EVAL_LIST_FILE | xargs -P $MAXPARALLEL -L 1 bash -c 'pypy ocr-evaluation-xargs.py /tmp/ocr-output-words.tsv $EVAL_DIR eval-results/deepdive/$0.txt $0'

cat eval-results/deepdive/* > eval-results.txt

# pypy ocr-evaluation-strict.py /tmp/ocr-output-words.tsv $EVAL_DIR eval-results.txt

# echo 'Evaluating Tesseract:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-tesseract.tsv data/test-evaluation/ output-tess/ eval-results-tess.txt
# echo 'Evaluating Cuneiform:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform.tsv data/test-evaluation/ output-cuni/ eval-results-cuni.txt

