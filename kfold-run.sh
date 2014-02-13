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

# Set the k-fold K here (4)
for iter in {1..4}; 
do 
  # Export the current kfold iteration
  export KFOLD_ITER=$iter 
  export KFOLD_NUM=4
  SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"
  rm -rf $DEEPDIVE_HOME/target/calibration-$iter
  mv $DEEPDIVE_HOME/target/calibration $DEEPDIVE_HOME/target/calibration-$iter
  psql -c """drop view if exists compare_results;
    create view compare_results as
    select lt.docid, lt.wordid, lt.probability as p_t, lc.probability as p_c
    from filtered_labels_label_t_inference as lt INNER JOIN filtered_labels_label_c_inference as lc ON lt.docid =lc.docid and lt.wordid=lc.wordid;

    (select count(*) from compare_results INNER JOIN labels 
    ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid);
    """ $DBNAME


done
