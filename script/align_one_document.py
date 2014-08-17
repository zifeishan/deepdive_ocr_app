import os, sys
from alignment import *

help = '''
This script processes Raw OCR results to aligned journal files.
Raw candidates directory is taken as input.

Arguments:
  docid: a unique string that identifies the document
  output_base: directory that stores the output *.cand
  input_bases: directory that may contain 
      input.text (Tess) and 
      *.html     (Cuni), 
    can be multiple directories.

e.g.
  python2.7 align_one_document.py 4968.2 test4968/ /lfs/madmax/0/czhang/paleopaleo/input_large_compact/4968.2/
'''
if __name__ == "__main__": 
  if len(sys.argv) >= 4:
    docid = sys.argv[1]
    output_base = sys.argv[2]
    input_bases = sys.argv[3:]

    if not os.path.exists(output_base):
      os.makedirs(output_base)
    
    # Align each file
    print 'Aligning', docid, '...'
    # Already aligned (cand file not empty), skip
    candpath = output_base + '/' + docid + '.cand'
    if os.path.exists(candpath) and os.path.getsize(candpath) > 0:
      print docid, 'already processed, skipped.'
    else:
      findpaths = input_bases
      Align.AlignBoxedFromPath(findpaths, docid, output_base)

  else:
    print 'This script needs SNAP library.'
    print help
    # 'Usage: python2.7',sys.argv[0],'<input_base> <docid> <output_base>'
    # print 'e.g.: python2.7',sys.argv[0],'data/html-labels-accurate/ground-truth-url.txt', './journals-output'
    sys.exit(1)
