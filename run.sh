#! /bin/bash

export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}

# cd data/raw/
# ROOT_PATH=`pwd`
# python gen_feature_table.py

cd "$(dirname $0)/../../";
ROOT_PATH=`pwd`

# $ROOT_PATH/app/ocr/prepare_data.sh

env SBT_OPTS="-Xmx4g" sbt "run -c app/ocr/application.conf"

cd "$(dirname $0)"
ROOT_PATH=`pwd`
python feature-analysis.py
