set -e
./run-bestpick.sh
./run-ocr-evaluation.sh
# ./run-evaluation.sh

# mkdir evaluation/bestpick-eval-old2
# mv evaluation/bestpick-evalgen.txt evaluation/bestpick-optimal-fuzzy evaluation/bestpick-cuni-eval-100.txt evaluation/bestpick-tess-eval-100.txt evaluation/bestpick-eval-old2/

mkdir -p evaluation/$DBNAME/bestpick-optimal-fuzzy/
# export BESTPICK_DIR=/lfs/local/0/zifei/bestpick-result/
cat $BESTPICK_DIR/*.stat.0 > evaluation/$DBNAME/bestpick-optimal-fuzzy/opt.0.txt
cat $BESTPICK_DIR/opt1/*.stat.0 > evaluation/$DBNAME/bestpick-optimal-fuzzy/opt.1.txt
cat $BESTPICK_DIR/opt2/*.stat.0 > evaluation/$DBNAME/bestpick-optimal-fuzzy/opt.2.txt
cat $BESTPICK_DIR/opt3/*.stat.0 > evaluation/$DBNAME/bestpick-optimal-fuzzy/opt.3.txt

cp eval-results-tess.txt evaluation/$DBNAME/
cp eval-results-cuni.txt evaluation/$DBNAME/

cat $BESTPICK_EVALGEN_DIR/*.stat.0 > evaluation/$DBNAME/bestpick-evalgen.txt

python plotting/plot-candgen-bestpick.py
