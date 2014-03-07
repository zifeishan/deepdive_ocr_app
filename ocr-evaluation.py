import os, sys

dd_output = '/tmp/ocr-output-words.tsv'
eval_path_base = 'data/test-supervision/'
final_output_base = 'output/'
if len(sys.argv) == 4:
  dd_output = sys.argv[1]
  eval_path_base = sys.argv[2]
  final_output_base = sys.argv[3]
else:
  print 'Usage: python', sys.argv[0],'dd_output eval_path_base final_output_base'
  print 'Use default settings.'

print 'Generating output from', dd_output,'to:',final_output_base

docids = []
lastdocid = ''
fout = None
while True:
  line = open(dd_output).readline()
  if line == '': break
  docid, wordid, word = line.strip().split('\t')
  wordid = int(wordid)

  # New document encountered
  if docid != lastdocid:
    docids.append(docid)
    if fout != None:
      fout.close()
    fout = open(final_output_base + '/' + docid + '.seq', 'w')

  print >>fout, word

if fout != None:
  fout.close()

fout = open('eval-results.txt', 'w')
sys.path.append('util/')
import stringmatch  # Use our script here

tot_ocrwords = 0
tot_evalwords = 0
tot_matchnum = 0

for docid in docids:
  ocrpath = final_output_base + '/' + docid + '.seq'
  evalpath = eval_path_base + '/' + docid + '.seq'
  if not os.path.exists(ocrpath):
    print 'Error: cannot find path:',ocrpath
    continue
  if not os.path.exists(evalpath):
    print 'Error: cannot find path:',evalpath
    continue
  ocrwords = [l.rstrip('\n') for l in open(ocrpath).readlines()]
  evalwords = [l.rstrip('\n') for l in open(evalpath).readlines()]
  matchnum = stringmatch.Match(ocrwords, evalwords)
  tot_ocrwords += len(ocrwords)
  tot_evalwords += len(evalwords)
  tot_matchnum += matchnum

  print '%s:\t OCR:%d\tReal:%d\tMatches:%d\tPrec:%.4f\tRec:%.4f' % [docid, 
      len(ocrwords), 
      len(evalwords), 
      matchnum, 
      matchnum / float(len(ocrwords)), 
      matchnum / float(len(evalwords))]

  print >>fout, '\t'.join ([str(x) for x in [docid, 
          len(ocrwords), 
          len(evalwords), 
          matchnum, 
          matchnum / float(len(ocrwords)), 
          matchnum / float(len(evalwords))]])

print 'TOTAL:\n%s:\t OCR:%d\tReal:%d\tMatches:%d\tPrec:%.4f\tRec:%.4f' % [docid, 
      tot_ocrwords, 
      tot_evalwords, 
      tot_matchnum, 
      tot_matchnum / float(tot_ocrwords), 
      tot_matchnum / float(tot_evalwords)]

fout.close()