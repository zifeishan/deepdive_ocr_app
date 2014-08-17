set -e

if [ $# != 1 ]; then
  echo "Usage: $0 docid_list"
  exit;
fi

EVAL_LIST_FILE=$1

if [ -z "$JOURNAL_DIR" ]; then # if empty
  export JOURNAL_DIR=/dfs/hulk/0/zifei/ocr/journals-output/
fi

if [ -z "$EVAL_DIR" ]; then # if empty
  export EVAL_DIR=/dfs/hulk/0/zifei/ocr/evaluation_escaped/
fi
if [ -z "$MAX_PARALLELISM" ]; then # if empty
  export MAX_PARALLELISM=25
fi

# pypy ocr-evaluation-strict.py $EXPORT_ROOT/ocr-output-words.tsv $EVAL_DIR eval-results.txt

echo 'Evaluating Tesseract...'

cat $EVAL_LIST_FILE | xargs -P $MAX_PARALLELISM -L 1 bash -c '
pypy ocr-evaluation-raw-candword.py $JOURNAL_DIR/$0.cand_word $EVAL_DIR/$0.seq ~/zifei/tess-eval-results/$0.stat T'

cat eval-results/tesseract/* > eval-results-tess.txt

