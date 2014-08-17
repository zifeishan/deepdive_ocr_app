SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_DIR/default.sh

export DBNAME=ddocr_100_textid
export PGHOST=rambo
export PGPORT=5433
export SUPV_GRAM_LEN=3