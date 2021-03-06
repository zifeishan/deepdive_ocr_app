SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_DIR/default.sh

export DBNAME=ddocr_30
export DB_NAME=$DBNAME
# export PGHOST=localhost
export PGHOST=0.0.0.0
export PGPORT=5432
export SUPV_GRAM_LEN=3
export SUPV_DIR=/Users/Robin/ssh-afs-deepdive/app/ocr/data/test-supv-eval-doc30/supervision/
export EVAL_DIR=/Users/Robin/ssh-afs-deepdive/app/ocr/data/test-supv-eval-doc30/evaluation/
export MAX_PARALLELISM=2
export BESTPICK_DIR=/Users/Robin/ssh-afs-deepdive/app/ocr/data/bestpick-results-local/
export BESTPICK_SAMPLE_SIZE=3000