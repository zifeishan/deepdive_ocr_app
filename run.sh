#! /bin/bash

export DBNAME=ddocr
export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export PG_PORT=${PGPORT:5432}

export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`
export APP_HOME=`pwd`
export JAVA_OPTS="-Xmx4g"

# $APP_HOME/prepare_data.sh

export CALI_FRACTION=0.25
export KFOLD_ITER=1
export KFOLD_NUM=4
# Only fold a fraction of data, TODO

export FEATURE_LIB_PATH=$APP_HOME/script/
export FEATURE_CONF_PATH=$APP_HOME/script/extract-feature-list.conf

cd $DEEPDIVE_HOME

SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"
# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application-old.conf"
