export SAMPLE_SIZE=3000
# # bash generate_ocr_result.sh
# # scp rocky:/tmp/ocr-output* /tmp/
# # pypy ocr-evaluation.py
# EVAL_DIR=/dfs/madmax5/0/zifei/deepdive/app/ocr/data/evaluation/
# # EVAL_DIR=data/test-evaluation

# echo 'Evaluating Tesseract:'
# pypy ocr-evaluation-strict.py /tmp/ocr-output-words-tesseract.tsv $EVAL_DIR eval-results-tess.txt
# echo 'Evaluating Cuneiform:'
# pypy ocr-evaluation-strict.py /tmp/ocr-output-words-cuneiform.tsv $EVAL_DIR eval-results-cuni.txt


if [ "$#" -ne 1 ]; then
    echo "Usage: ... <dbname>. (uses PGHOST)"
else
  DBNAME=$1
fi
bash generate_ocr_result.sh $DBNAME

# export EXPORT_ROOT='/dfs/hulk/0/zifei/ocr/tmp/'

if [ $PGHOST != "localhost" ]; then
  echo "Copying files from $PGHOST"
  scp $PGHOST:/tmp/ocr-output* /tmp/
fi

export EXPORT_ROOT=/tmp/

### pypy ocr-evaluation.py
# EVAL_DIR=/dfs/madmax5/0/zifei/deepdive/app/ocr/data/evaluation/
# EVAL_DIR=/dfs/madmax/0/zifei/deepdive/app/ocr/data/evaluation/
# EVAL_DIR=data/test-evaluation

mkdir -p eval-results/tesseract/ eval-results/cuneiform/
rm -f eval-results/tesseract/*
rm -f eval-results/cuneiform/*

# export MAXPARALLEL=25
export EVAL_LIST_FILE=$EXPORT_ROOT/ocr-eval-docs.tsv
if [ -z "$SUPV_DIR" ]; then # if empty
  export SUPV_DIR=/dfs/hulk/0/zifei/ocr/supervision_escaped/
fi

if [ -z "$EVAL_DIR" ]; then # if empty
  export EVAL_DIR=/dfs/hulk/0/zifei/ocr/evaluation_escaped/
fi
if [ -z "$MAX_PARALLELISM" ]; then # if empty
  export MAX_PARALLELISM=25
fi

# pypy ocr-evaluation-strict.py $EXPORT_ROOT/ocr-output-words.tsv $EVAL_DIR eval-results.txt


cat $EVAL_LIST_FILE | xargs -P $MAXPARALLEL -L 1 bash -c 'pypy ocr-evaluation-xargs.py $EXPORT_ROOT/ocr-output-words-tesseract.tsv $EVAL_DIR eval-results/tesseract/$0.txt $0 $SAMPLE_SIZE'

cat eval-results/tesseract/* > eval-results-tess.txt

cat $EVAL_LIST_FILE | xargs -P $MAXPARALLEL -L 1 bash -c 'pypy ocr-evaluation-xargs.py $EXPORT_ROOT/ocr-output-words-cuneiform.tsv $EVAL_DIR eval-results/cuneiform/$0.txt $0 $SAMPLE_SIZE'

cat eval-results/cuneiform/* > eval-results-cuni.txt

# pypy ocr-evaluation-strict.py $EXPORT_ROOT/ocr-output-words.tsv $EVAL_DIR eval-results.txt

# echo 'Evaluating Tesseract:'
# pypy ocr-evaluation.py $EXPORT_ROOT/ocr-output-words-tesseract.tsv data/test-evaluation/ output-tess/ eval-results-tess.txt
# echo 'Evaluating Cuneiform:'
# pypy ocr-evaluation.py $EXPORT_ROOT/ocr-output-words-cuneiform.tsv data/test-evaluation/ output-cuni/ eval-results-cuni.txt

