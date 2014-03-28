# bash generate_ocr_result.sh
# scp rocky:/tmp/ocr-output* /tmp/
# pypy ocr-evaluation.py
echo 'Evaluating Tesseract:'
pypy ocr-evaluation.py /tmp/ocr-output-words-tesseract.tsv data/test-evaluation/ output-tess/ eval-results-tess.txt
echo 'Evaluating Cuneiform:'
pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform.tsv data/test-evaluation/ output-cuni/ eval-results-cuni.txt

