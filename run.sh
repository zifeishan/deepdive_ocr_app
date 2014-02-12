#! /bin/bash

export DBNAME=ddocr
export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export PG_PORT=5432

export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`
export APP_HOME=`pwd`
export JAVA_OPTS="-Xmx4g"


# cd data/raw/
# ROOT_PATH=`pwd`
# python gen_feature_table.py

cd "$(dirname $0)/../../";
ROOT_PATH=`pwd`

# $ROOT_PATH/app/ocr/prepare_data.sh

SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"

# cd "$(dirname $0)"
# ROOT_PATH=`pwd`
# python feature-analysis.py
