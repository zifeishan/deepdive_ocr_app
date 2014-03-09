import os, sys
from alignment import *

if __name__ == "__main__": 
  if len(sys.argv) == 3:
    inputurls = sys.argv[1]
    output_base = sys.argv[2]

    if not os.path.exists(output_base):
      os.makedirs(output_base)

    fids = [s.strip().split('\t')[0] for s in open(inputurls).readlines()]

    firstdir = '/dfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_feb15/'
    seconddir = '/dfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_JOURNAL/'

    print fids[:100]
    
    # Align each file
    for fid in fids:
      # Already aligned (cand file not empty), skip
      candpath = output_base + '/' + fid + '.cand'
      if os.path.exists(candpath) and os.path.getsize(candpath) > 0:
        print fid, 'already processed, skipped.'
        continue

      findpaths = [firstdir + fid + '.pdf.task/', seconddir + fid + '.pdf.task/']
      Align.AlignBoxedFromPath(findpaths, fid, output_base)

    # AlignBoxedFromPath(path, 'JOURNAL_28971', './test')
  else:
    print 'Usage:',sys.argv[0],'<procfiles> <output_base>'
    print 'e.g.:',sys.argv[0],'data/html-labels-accurate/ground-truth-url.txt', './journals-output'
    sys.exit(1)
