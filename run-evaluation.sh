if [ "$#" -ne 1 ]; then
    echo "Usage: ... <dbname>. (uses PGHOST)"
fi
bash generate_ocr_result.sh $1
scp $PGHOST:/tmp/ocr-output* /tmp/
### pypy ocr-evaluation.py
# EVAL_DIR=/dfs/madmax5/0/zifei/deepdive/app/ocr/data/evaluation/
EVAL_DIR=/dfs/madmax/0/zifei/deepdive/app/ocr/data/evaluation/
# EVAL_DIR=data/test-evaluation
pypy ocr-evaluation-strict.py /tmp/ocr-output-words.tsv $EVAL_DIR eval-results.txt

# echo 'Evaluating Tesseract:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-tesseract.tsv data/test-evaluation/ output-tess/ eval-results-tess.txt
# echo 'Evaluating Cuneiform:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform.tsv data/test-evaluation/ output-cuni/ eval-results-cuni.txt

