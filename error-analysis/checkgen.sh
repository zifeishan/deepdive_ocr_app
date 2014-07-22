export DOCID='JOURNAL_40091'

export OPT_MATCH_DIR='/lfs/local/0/zifei/bestpick-result'
export GEN_RES_DIR='/lfs/local/0/zifei/bestpick-evalgen'
# export GEN_RES_DIR='/dfs/madmax2/0/zifei/bestpick-result-domain1gram'
# export GEN_RES_DIR='/dfs/madmax2/0/zifei/bestpick-result-google1gram'

# echo $#

if [ $# = 1 ]; then
  export DOCID=$1
  echo "DOCID set to $1"
fi

if [ $# = 2 ]; then
  export DOCID=$1
  export GEN_RES_DIR=$2
fi

vimdiff $OPT_MATCH_DIR/$DOCID.matches.0 $GEN_RES_DIR/$DOCID.matches.0 $OPT_MATCH_DIR/$DOCID.matches.1

# vimdiff $GEN_RES_DIR/$DOCID.matches.0 $OPT_MATCH_DIR/$DOCID.matches.1 $OPT_MATCH_DIR/$DOCID.matches.2
