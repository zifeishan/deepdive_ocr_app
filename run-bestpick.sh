#! /bin/bash

if hash psql 2>/dev/null; then  # check psql exists
    true
else
    echo 'ERROR: psql does not exist.'
    exit
fi

if [ $# = 2 ]; then          # Export DBNAME from command line
  export SUPV_GRAM_LEN=$1
  export DBNAME=$2
fi

if [ -z "$DBNAME" ]; then # if empty
  echo 'ERROR: DBNAME is unset.'
  echo 'Usage: '$0' SUPV_GRAM_LEN DBNAME'
  exit
fi

export PGDATABASE=$DBNAME

# export DBNAME=ddocr
# export DBNAME=ddocr_large
export DB_NAME=${DBNAME}
export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export PG_PORT=${PGPORT:5432}
if [ -z "$BESTPICK_DIR" ]; then # if empty
  export BESTPICK_DIR=/lfs/local/0/zifei/bestpick-result/
  echo "Bestpick dir: $BESTPICK_DIR"
fi

echo "Set DB_NAME to ${DBNAME}."
echo "HOST is ${PGHOST}, PORT is ${PGPORT}."
echo "Supervision ngram: ${SUPV_GRAM_LEN}"

export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`
export APP_HOME=`pwd`
# export JAVA_OPTS="-Xmx128g -XX:MaxHeapSize=256m"
# export JAVA_OPTS="-Xmx128g -XX:MaxHeapSize=8g"

# java $JAVA_OPTS -version

# $APP_HOME/prepare_data.sh
# 20 have resource problem
# export MAX_PARALLELISM=15
export CALI_FRACTION=0.25
export KFOLD_ITER=1
export KFOLD_NUM=4
# Only fold a fraction of data, TODO

export FEATURE_LIB_PATH=$APP_HOME/script/
export FEATURE_CONF_PATH=$APP_HOME/script/extract-feature-list.conf
export LD_LIBRARY_PATH="/dfs/rulk/0/hazy_share/lib64/:/dfs/rulk/0/hazy_share/lib/protobuf/lib/:/dfs/rulk/0/hazy_share/lib/tclap/lib/:$LD_LIBRARY_PATH"
export DICT_FILE=$APP_HOME/util/words

# export SUPV_DIR=$APP_HOME/data/test-supervision
# # export SUPV_DIR=$APP_HOME/data/test-evaluation  # for testing optimal picking

if [ -z "$SUPV_DIR" ]; then # if empty
  export SUPV_DIR=/dfs/hulk/0/zifei/ocr/supervision_escaped/
fi

if [ -z "$EVAL_DIR" ]; then # if empty
  export EVAL_DIR=/dfs/hulk/0/zifei/ocr/evaluation_escaped/
fi
if [ -z "$MAX_PARALLELISM" ]; then # if empty
  export MAX_PARALLELISM=15
fi

cd $DEEPDIVE_HOME

echo 'Running SBT...'
# SBT_OPTS="-Xmx128g -XX:MaxHeapSize=8g" sbt/sbt "run -c $APP_HOME/application.conf"
# SBT_OPTS="-Xmx128g" sbt/sbt "run -c $APP_HOME/application.conf"
deepdive -c $APP_HOME/bestpick.conf

# SBT_OPTS="-Xmx2g -XX:MaxHeapSize=2g" sbt/sbt "run -c $APP_HOME/application-develop.conf"


# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"
# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application-old.conf"

# cd $APP_HOME
# bash generate_ocr_result.sh
# scp rocky:/tmp/ocr-output* /tmp/
# pypy ocr-evaluation.py
# echo 'Evaluating Tesseract:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-tesseract.tsv data/test-evaluation/ output-tess/ eval-results-tess.txt
# echo 'Evaluating Cuneiform:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform.tsv data/test-evaluation/ output-cuni/ eval-results-cuni.txt

cd $APP_HOME
# ./run-evaluation.sh
# python plot-eval-recall.py

# mkdir -p evaluation/bestpick-optimal-fuzzy/
# cat $BESTPICK_DIR/*.stat.0 > evaluation/bestpick-optimal-fuzzy/opt.0.txt
# cat $BESTPICK_DIR/*.stat.1 > evaluation/bestpick-optimal-fuzzy/opt.1.txt
# cat $BESTPICK_DIR/*.stat.2 > evaluation/bestpick-optimal-fuzzy/opt.2.txt
# cat $BESTPICK_DIR/*.stat.3 > evaluation/bestpick-optimal-fuzzy/opt.3.txt
# cat $BESTPICK_DIR/*.stat.4 > evaluation/bestpick-optimal-fuzzy/opt.4.txt
# cat $BESTPICK_DIR/*.stat.5 > evaluation/bestpick-optimal-fuzzy/opt.5.txt

# mkdir -p evaluation/bestpick-optimal-fuzzy-trgm/
# cat $BESTPICK_DIR/*.stat.0.1 > evaluation/bestpick-optimal-fuzzy-trgm/opt.0.1.txt
# cat $BESTPICK_DIR/*.stat.0.3 > evaluation/bestpick-optimal-fuzzy-trgm/opt.0.3.txt
# cat $BESTPICK_DIR/*.stat.0.5 > evaluation/bestpick-optimal-fuzzy-trgm/opt.0.5.txt
# cat $BESTPICK_DIR/*.stat.0.7 > evaluation/bestpick-optimal-fuzzy-trgm/opt.0.7.txt
# cat $BESTPICK_DIR/*.stat.0.9 > evaluation/bestpick-optimal-fuzzy-trgm/opt.0.9.txt
