if hash psql 2>/dev/null; then  # check psql exists
    true
else
    echo 'ERROR: psql does not exist.'
    exit
fi

# export EXPORT_ROOT='/dfs/hulk/0/zifei/ocr/tmp/'
export EXPORT_ROOT='/tmp/'

# DOCID='JOURNAL_13504'
DOCID='JOURNAL_45432'
TRANSCRIPT_DIR='/dfs/hulk/0/zifei/ocr/evaluation_escaped/'   # Compare to transcript
OPTIMAL_DIR='../evaluation/bestpick-result/'								# Compare to optimal

COMPARE_METHOD='1'    # 1: dd-optimal 2: dd-transcript 3: optimal-transcript

if [ $# > 0 ]; then
  export DOCID=$1
fi
if [ $# > 1 ]; then
  export COMPARE_METHOD=$2
fi

grep $DOCID $EXPORT_ROOT/ocr-output-words.tsv | cut -f 3 > tmp-dd-output.tsv

if [ $COMPARE_METHOD = '1' ]; then
	vimdiff -R tmp-dd-output.tsv $OPTIMAL_DIR/$DOCID.seq
fi
if [ $COMPARE_METHOD = '2' ]; then
	vimdiff -R tmp-dd-output.tsv $TRANSCRIPT_DIR/$DOCID.seq
fi
if [ $COMPARE_METHOD = '3' ]; then
	vimdiff -R $OPTIMAL_DIR/$DOCID.seq $TRANSCRIPT_DIR/$DOCID.seq
fi
if [ $COMPARE_METHOD = '0' ]; then
	vimdiff -R tmp-dd-output.tsv $OPTIMAL_DIR/$DOCID.seq $TRANSCRIPT_DIR/$DOCID.seq
fi