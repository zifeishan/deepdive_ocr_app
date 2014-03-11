bash generate_ocr_result.sh
scp zifei@rocky:/tmp/ocr-output-words* /tmp/
pypy ocr-evaluation.py
# echo 'Evaluating Tesseract:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-tesseract.tsv data/test-supervision/ output-tess/ eval-results-tess.txt
# echo 'Evaluating Cuneiform:'
# pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform.tsv data/test-supervision/ output-cuni/ eval-results-cuni.txt