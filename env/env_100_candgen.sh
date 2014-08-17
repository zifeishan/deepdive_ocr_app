SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_DIR/default.sh
export DBNAME=ddocr_100_candgen
export PGHOST=rambo
export PGPORT=5433
export SUPV_GRAM_LEN=3
export SUPV_DIR=/dfs/hulk/0/zifei/ocr/supervision_escaped/
export EVAL_DIR=/dfs/hulk/0/zifei/ocr/evaluation_escaped/
export BESTPICK_DIR=/lfs/local/0/zifei/ddocr_100/bestpick-result/
export BESTPICK_EVALGEN_DIR=/lfs/local/0/zifei/ddocr_100/bestpick-evalgen/