SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_DIR/default.sh
# echo "Please also do: . env/default.sh"

export DBNAME=ddocr_4968
export PGHOST=rambo
export PGPORT=5433
export CAND_DIR=/afs/cs.stanford.edu/u/zifei/repos/deepdive/app/ocr/script/test4968/
export SUPV_DIR=/afs/cs.stanford.edu/u/zifei/repos/deepdive/app/ocr/data/original-error-analysis-documents/evaluation_seq
export EVAL_DIR=/afs/cs.stanford.edu/u/zifei/repos/deepdive/app/ocr/data/original-error-analysis-documents/evaluation_seq
export KFOLD_NUM=1  # holdout all the docs
# all for evaluation
export BESTPICK_DIR=/lfs/local/0/zifei/4968-corpus/bestpick-result/
export BESTPICK_EVALGEN_DIR=/lfs/local/0/zifei/4968-corpus/bestpick-evalgen/
export SUPV_GRAM_LEN=3
export TSV_EXT_BATCH_SIZE=1