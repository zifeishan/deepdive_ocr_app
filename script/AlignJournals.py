import os, sys

if __name__ == "__main__": 
  if len(sys.argv) == 3:
    inputurls = sys.argv[1]
    output_base = sys.argv[2]

    if not os.path.exists(output_base):
      os.makedirs(output_base)

    fids = [s.split('\t')[0] for s in open(inputurls).readlines()]

    firstdir = '/lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_feb15/'
    seconddir = '/lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_JOURNAL/'

    print fids[:100]
    # raw_input()

    ferr = open('errlog.txt', 'w')
    for fid in fids:
      if os.path.exists(firstdir + fid):
        path = firstdir + fid
      elif os.path.exists(seconddir + fid):
        path = seconddir + fid 
      else:
        print 'Unable to find file:', fid
        print >>ferr, 'Unable to find file:', fid
        ferr.flush()
        continue
      AlignBoxedFromPath(path, fid, output_base)

    # AlignBoxedFromPath(path, 'JOURNAL_28971', './test')
  else:
    print 'Usage:',sys.argv[0],'<procfiles> <output_base>'
    print 'e.g.:',sys.argv[0],'data/html-labels-accurate/ground-truth-url.txt', './journals-output'
    sys.exit(1)
