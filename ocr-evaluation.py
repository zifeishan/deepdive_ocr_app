import os, sys

print '''THIS SCRIPT IS DEPRECATED. Use ocr-evaluation-strict.py instead!!'''

# Use stanford tokenizer to segment before alignment
SEGMENT_CMD = 'CLASSPATH=util/stanford-parser.jar java edu.stanford.nlp.process.PTBTokenizer -options "ptb3Escaping=false" '

dd_output = '/tmp/ocr-output-words.tsv'
eval_path_base = 'data/test-evaluation/'
final_output_base = 'output/'
output_stat_path = 'eval-results.txt'

if len(sys.argv) >= 5:
  dd_output = sys.argv[1]
  eval_path_base = sys.argv[2]
  final_output_base = sys.argv[3]
  output_stat_path = sys.argv[4]
else:
  print 'Usage: python', sys.argv[0],'dd_output eval_path_base final_output_base output_stat_path [docid_list]'
  print 'e.g. pypy ocr-evaluation.py /tmp/ocr-output-words-cuneiform.tsv data/test-evaluation/ output-cuni/ eval-results-cuni.txt'
  print 'Use default settings.'

docid_filter = None
if len(sys.argv) == 6:
  docidlist_path = sys.argv[5]
  docid_filter = [l.strip() for l in open(docidlist_path).readlines()] 
print 'Generating output from', dd_output,'to:',final_output_base

docids = []
lastdocid = ''
fout = None
fin = open(dd_output)
while True:
  line = fin.readline()
  if line == '': break
  docid, wordid, word = line.strip().split('\t')
  # wordid = int(wordid)

  # New document encountered
  if docid != lastdocid:
    print 'Reading doc:', docid
    docids.append(docid)
    lastdocid = docid
    if fout != None:
      fout.close()
    fout = open(final_output_base + '/' + docid + '.seq_unsegmented', 'w')

  print >>fout, word

if fout != None:
  fout.close()
fin.close()

fout = open(output_stat_path, 'w')
sys.path.append('util/')
import stringmatch  # Use our script here

tot_ocrwords = 0
tot_evalwords = 0
tot_matchnum = 0

# Only evaluate these documents
if docid_filter != None:
  docids = docid_filter


'NOTICE: DO NOT RESEGMENT.'

for docid in docids:
  ocrpath = final_output_base + '/' + docid + '.seq_unsegmented'
  evalpath = eval_path_base + '/' + docid + '.seq'
  if not os.path.exists(ocrpath):
    print 'Error: cannot find path:',ocrpath
    continue
  if not os.path.exists(evalpath):
    print 'Error: cannot find path:',evalpath
    continue
  # # DO NOT RESEGMENT
  # os.system(SEGMENT_CMD +' <' + final_output_base + '/' + docid + '.seq_unsegmented' + ' >' + final_output_base + '/' + docid + '.seq' )

  # ocrpath_segmented = final_output_base + '/' + docid + '.seq'
  # # DO NOT RESEGMENT
  ocrpath_segmented = final_output_base + '/' + docid + '.seq_unsegmented'

  ocrwords = [l.rstrip('\n') for l in open(ocrpath_segmented).readlines()]

  evalwords = [l.rstrip('\n') for l in open(evalpath).readlines()]
  matchnum = stringmatch.Match(ocrwords, evalwords)
  tot_ocrwords += len(ocrwords)
  tot_evalwords += len(evalwords)
  tot_matchnum += matchnum

  print '%s:\t OCR:%d\tReal:%d\tMatches:%d\tPrec:%.4f\tRec:%.4f' % (docid, 
      len(ocrwords), 
      len(evalwords), 
      matchnum, 
      matchnum / float(len(ocrwords)), 
      matchnum / float(len(evalwords))
      )

  print >>fout, '\t'.join ([str(x) for x in [docid, 
          len(ocrwords), 
          len(evalwords), 
          matchnum, 
          matchnum / float(len(ocrwords)), 
          matchnum / float(len(evalwords))]])

print 'TOTAL:\n%s:\t OCR:%d\tReal:%d\tMatches:%d\tPrec:%.4f\tRec:%.4f' % (docid, 
      tot_ocrwords, 
      tot_evalwords, 
      tot_matchnum, 
      tot_matchnum / float(tot_ocrwords), 
      tot_matchnum / float(tot_evalwords))

fout.close()