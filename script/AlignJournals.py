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
    # raw_input()

    ferr = open('errlog.txt', 'w')
    for fid in fids:
      findpaths = [firstdir + fid + '.pdf.task/', seconddir + fid + '.pdf.task/']
      Align.AlignBoxedFromPath(findpaths, fid, output_base)

    # AlignBoxedFromPath(path, 'JOURNAL_28971', './test')
  else:
    print 'Usage:',sys.argv[0],'<procfiles> <output_base>'
    print 'e.g.:',sys.argv[0],'data/html-labels-accurate/ground-truth-url.txt', './journals-output'
    sys.exit(1)
