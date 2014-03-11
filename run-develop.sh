#! /bin/bash
alias java='/lfs/local/0/dbritz/software/jdk1.7.0_51/bin/java'
export DBNAME=ddocr
export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export PG_PORT=${PGPORT:5432}

export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`
export APP_HOME=`pwd`
# export JAVA_OPTS="-Xmx128g -XX:MaxHeapSize=256m"
# export JAVA_OPTS="-Xmx128g -XX:MaxHeapSize=8g"

# java $JAVA_OPTS -version

# $APP_HOME/prepare_data.sh

export CALI_FRACTION=0.25
export KFOLD_ITER=1
export KFOLD_NUM=4
# Only fold a fraction of data, TODO

export FEATURE_LIB_PATH=$APP_HOME/script/
export FEATURE_CONF_PATH=$APP_HOME/script/extract-feature-list.conf
export LD_LIBRARY_PATH="/dfs/rulk/0/hazy_share/lib64/:/dfs/rulk/0/hazy_share/lib/protobuf/lib/:/dfs/rulk/0/hazy_share/lib/tclap/lib/:$LD_LIBRARY_PATH"

cd $DEEPDIVE_HOME

# SBT_OPTS="-Xmx128g -XX:MaxHeapSize=8g" sbt/sbt "run -c $APP_HOME/application.conf"
SBT_OPTS="-Xmx32g" sbt/sbt "run -c $APP_HOME/application-develop.conf"

# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"
# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application-old.conf"

# cd $APP_HOME
# bash generate_ocr_result.sh
# pypy ocr-evaluation.py
# echo 'Evaluating Tesseract:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-tesseract.tsv data/test-supervision/ output-tess/ eval-results-tess.txt
# echo 'Evaluating Cuneiform:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform.tsv data/test-supervision/ output-cuni/ eval-results-cuni.txt
