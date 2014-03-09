#! /bin/bash
alias java='/lfs/local/0/dbritz/software/jdk1.7.0_51/bin/java'
export DBNAME=ddocr
export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export PG_PORT=${PGPORT:5432}

export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`
export APP_HOME=`pwd`
# export JAVA_OPTS="-Xmx128g -XX:MaxHeapSize=256m"
export JAVA_OPTS="-Xmx128g -XX:MaxHeapSize=8g"

# java $JAVA_OPTS -version

# $APP_HOME/prepare_data.sh

export CALI_FRACTION=0.25
export KFOLD_ITER=1
export KFOLD_NUM=4
# Only fold a fraction of data, TODO

export FEATURE_LIB_PATH=$APP_HOME/script/
export FEATURE_CONF_PATH=$APP_HOME/script/extract-feature-list.conf

cd $DEEPDIVE_HOME

# SBT_OPTS="-Xmx128g -XX:MaxHeapSize=8g" sbt/sbt "run -c $APP_HOME/application.conf"
SBT_OPTS="-Xmx128g" sbt/sbt "run -c $APP_HOME/application.conf"

# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"
# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application-old.conf"

cd $APP_HOME

# bash generate_ocr_result.sh
# pypy ocr-evaluation.py