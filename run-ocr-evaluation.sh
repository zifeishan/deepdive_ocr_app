# bash generate_ocr_result.sh
# scp rocky:/tmp/ocr-output* /tmp/
# pypy ocr-evaluation.py
EVAL_DIR=/dfs/madmax5/0/zifei/deepdive/app/ocr/data/evaluation/
# EVAL_DIR=data/test-evaluation

echo 'Evaluating Tesseract:'
pypy ocr-evaluation.py /tmp/ocr-output-words-tesseract.tsv $EVAL_DIR output-tess/ eval-results-tess.txt
echo 'Evaluating Cuneiform:'
pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform.tsv $EVAL_DIR output-cuni/ eval-results-cuni.txt

