SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_DIR/default.sh

export DBNAME=ddocr_dirty
export PGHOST=rambo
export PGPORT=5433
export SUPV_DIR=/dfs/hulk/0/zifei/ocr/supervision_escaped/
export EVAL_DIR=/dfs/hulk/0/zifei/ocr/evaluation_escaped/
export KFOLD_NUM=2
# all for evaluation
export BESTPICK_DIR=/lfs/local/0/zifei/dirty-corpus/bestpick-result/
export BESTPICK_EVALGEN_DIR=/lfs/local/0/zifei/dirty-corpus/bestpick-evalgen/