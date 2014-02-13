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

# Store stats...
rm -f evaluation.tsv

# Set the k-fold K here (4)
for iter in {1..4}; 
do 
  # Export the current kfold iteration
  export KFOLD_ITER=$iter 
  export KFOLD_NUM=4
  SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"
  rm -rf $DEEPDIVE_HOME/target/calibration-$iter
  mv $DEEPDIVE_HOME/target/calibration $DEEPDIVE_HOME/target/calibration-$iter
  python ocr-evaluation.py
  
done

rm -rf evaluation
mkdir evaluation
mv evaluation.tsv evaluation/
mv $DEEPDIVE_HOME/target/calibration-* evaluation/
cat evaluation/evaluation.tsv
