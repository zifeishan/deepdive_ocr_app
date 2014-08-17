# This env file is default for all db settings. env vars can be reloaded after this. We don't do envs in run.sh any more.

export CAND_DIR=/dfs/hulk/0/zifei/ocr/journals-output/
export SUPV_DIR=/dfs/hulk/0/zifei/ocr/supervision_escaped/
export EVAL_DIR=/dfs/hulk/0/zifei/ocr/evaluation_escaped/
export GOOGLE_1GRAM_TSV=/dfs/hulk/0/zifei/ocr/google-ngram/1gram.tsv
export GOOGLE_2GRAM_TSV=/dfs/hulk/0/zifei/ocr/google-ngram/2gram_reduced.tsv
export DOMAIN_CORPUS=/dfs/hulk/0/zifei/ocr/domain-corpus.tsv

export CALI_FRACTION=0.25
export KFOLD_ITER=1
if [ -z "$KFOLD_NUM" ]; then # if empty
  export KFOLD_NUM=4
fi
# Only fold a fraction of data, TODO


export CAND_GEN_DIST=2
export MAX_CAND_NUM=3
export MAX_COMB_STRLEN=20
export MAX_SEG_PARTS=5

# export SUPV_DIR=$APP_HOME/data/test-supervision
# # export SUPV_DIR=$APP_HOME/data/test-evaluation  # for testing optimal picking

export MAX_PARALLELISM=15
export SUPV_GRAM_LEN=3
export TSV_EXT_BATCH_SIZE=4