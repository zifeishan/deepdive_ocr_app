#! /bin/bash
alias java='/lfs/local/0/dbritz/software/jdk1.7.0_51/bin/java'
export DBNAME=ddocr
export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export PG_PORT=${PGPORT:5432}

export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`
export APP_HOME=`pwd`
export JAVA_OPTS="-Xmx4g -XX:MaxHeapSize=256m"

# java $JAVA_OPTS -version

# $APP_HOME/prepare_data.sh

export CALI_FRACTION=0.25
export KFOLD_ITER=1
export KFOLD_NUM=4
# Only fold a fraction of data, TODO

export FEATURE_LIB_PATH=$APP_HOME/script/
export FEATURE_CONF_PATH=$APP_HOME/script/extract-feature-list.conf

cd $DEEPDIVE_HOME

SBT_OPTS="-Xmx4g -XX:MaxHeapSize=256m" sbt/sbt "run -c $APP_HOME/application.conf"

# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"
# SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application-old.conf"

psql -c """ copy (select * from cand_label_label_inference_bucketed right join candidate on candidateid=candidate.id) to '/tmp/ocr-output-eval.tsv'; """ $DBNAME


 # select label, probability, bucket, candidate.* from cand_label_label_inference_bucketed right join candidate on candidateid=candidate.id;

 # select label, probability, bucket, candidate.* from cand_label_label_inference_bucketed right join candidate on candidateid=candidate.id where docid in (select * from eval_docs) and probability is not null;
