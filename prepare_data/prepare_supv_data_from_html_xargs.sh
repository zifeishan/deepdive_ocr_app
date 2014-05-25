if [ $# = 3 ]; then
  export supv_or_eval=$1
  export path=$2
  export outbase=$3
else
  echo 'Usage: '$0' <supv_or_eval> <path> <outbase>'
  echo 'e.g. '$0' supv ../data/html-labels-accurate/html/test-30docs/ ../data/test-supervision/'
  echo 'e.g. '$0' eval ../data/html-labels-accurate/html/test-30docs/ ../data/test-evaluation/'
  exit
fi

mkdir -p $outbase

export MAXPARALLEL=24

find $path*.html | xargs -P $MAXPARALLEL -L 1 bash -c 'pypy prepare_supv_data_from_html.py $supv_or_eval $0 $outbase'

# bash prepare_supv_data_from_html_xargs.sh supv /dfs/hulk/0/zifei/ocr/sd-html/ /dfs/hulk/0/zifei/ocr/supervision_escaped/
# bash prepare_supv_data_from_html_xargs.sh eval /dfs/hulk/0/zifei/ocr/sd-html/ /dfs/hulk/0/zifei/ocr/evaluation_escaped/