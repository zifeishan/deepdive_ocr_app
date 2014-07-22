# pypy stringmatch.py ../output-tess/$1.seq ../data/test-evaluation/$1.seq
grep $1 /tmp/ocr-output-words-tesseract.tsv | cut -f 3 > test/tess-output/$1.seq
echo "Saved to test/tess-output/$1.seq"
echo "Matching Tesseract with sequence using original stringmatch:"
echo pypy stringmatch.py test/tess-output/$1.seq /dfs/hulk/0/zifei/ocr/evaluation_escaped/$1.seq
pypy stringmatch.py test/tess-output/$1.seq /dfs/hulk/0/zifei/ocr/evaluation_escaped/$1.seq
# echo pypy candmatch.py test/tess-output/$1.seq /dfs/hulk/0/zifei/ocr/evaluation_escaped/$1.seq
# pypy candmatch.py test/tess-output/$1.seq /dfs/hulk/0/zifei/ocr/evaluation_escaped/$1.seq
