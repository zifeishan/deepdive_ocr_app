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
# OPTIMAL_DIR='../evaluation/bestpick-result/'								# Compare to optimal
OPTIMAL_DIR='/lfs/local/0/zifei/bestpick-evalgen/'                # Compare to optimal

COMPARE_METHOD='2'    # 1: dd-optimal 2: dd-transcript 3: optimal-transcript

if [ $# = 1 ]; then
  export DOCID=$1
fi
if [ $# = 2 ]; then
  export DOCID=$1
  export COMPARE_METHOD=$2
fi

grep $DOCID $EXPORT_ROOT/ocr-output-words.tsv | cut -f 3 > tmp-dd-output.tsv

if [ $COMPARE_METHOD = '1' ]; then
	vimdiff -R tmp-dd-output.tsv $OPTIMAL_DIR/$DOCID.seq.0
fi
if [ $COMPARE_METHOD = '2' ]; then
	vimdiff -R tmp-dd-output.tsv $TRANSCRIPT_DIR/$DOCID.seq
fi
if [ $COMPARE_METHOD = '3' ]; then
	vimdiff -R $OPTIMAL_DIR/$DOCID.seq.0 $TRANSCRIPT_DIR/$DOCID.seq
fi
# if [ $COMPARE_METHOD = 'debugmatch' ]; then
  ## starts with ".", matches
  # Not sure why it is problematic. ".matches.0 sometimes has error?"
  # grep -P "\.\t" $OPTIMAL_DIR/$DOCID.matches.0 | cut -f 2 > tmp-optimal.matches
  # grep -P "[^X]\t" $DOCID.matches.0 | cut -f 2 > tmp-optimal.matches
  # vimdiff -R $DOCID.seq.0 tmp-optimal.matches
# fi
if [ $COMPARE_METHOD = '0' ]; then
	vimdiff -R tmp-dd-output.tsv $OPTIMAL_DIR/$DOCID.seq.0 $TRANSCRIPT_DIR/$DOCID.seq
  # vimdiff -R tmp-dd-output.tsv tmp-optimal.matches $TRANSCRIPT_DIR/$DOCID.seq
fi
if [ $COMPARE_METHOD = '2d' ]; then
  diff tmp-dd-output.tsv $TRANSCRIPT_DIR/$DOCID.seq | grep '^>' | sort | uniq -c | sort -n | tail -n 20
fi
if [ $COMPARE_METHOD = '1d' ]; then
  diff tmp-dd-output.tsv $OPTIMAL_DIR/$DOCID.seq.0 | grep '^>' | sort | uniq -c | sort -n | tail -n 20
fi
if [ $COMPARE_METHOD = '3d' ]; then
  diff $OPTIMAL_DIR/$DOCID.seq.0 $TRANSCRIPT_DIR/$DOCID.seq | grep '^>' | sort | uniq -c | sort -n | tail -n 20
fi