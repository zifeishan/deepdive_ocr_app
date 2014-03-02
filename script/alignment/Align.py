import sys, os
from alignment import *

#deprecated
def AlignFromPath(dirbase, output_base):
  # sample of dirbase: '../../input/'
  Align(dirbase, output_base, isDir=True)

#deprecated
def AlignFromURL(urlbase, output_base):
  Align(urlbase, output_base, isDir=False)


# use this for madmax data.. Ce's output
# docid: identifier for doc, used in deepdive. e.g. 'JOURNAL_10'
# output_base: a directory for storing
# findpaths: in priority, good.
def AlignBoxedFromPath(findpaths, docid, output_base):
  # sample of dirbase: '../../input/'
  # AlignBoxedCunei(dirbase, output_base, isDir=True, boxedCunei = True)

  tess_dir = ''
  for dirbase in findpaths:
    if os.path.exists(dirbase + 'input.text'):
      tess_dir = dirbase + 'input.text'
      break

  cuni_dir = ''
  for dirbase in findpaths:
    if os.path.exists(dirbase + 'fonts.text'):
      cuni_dir = dirbase + 'fonts.text'
      break

  if tess_dir == '' or cuni_dir == '':
    print 'Cannot find output file for Tess / Cuni:', [tess_dir, cuni_dir]
    return
    
  print 'Loading OCR outputs from', dirbase
  twords = TessReader.ReadPath(tess_dir)
  cwords = BoxedCuneiReader.ReadPath(cuni_dir)
  print 'Align words...', dirbase
  tindex = Combiner.BuildBoxIndexByPage(twords)
  cindex = Combiner.BuildBoxIndexByPage(cwords)
  allwords = {'T': tindex, 'C': cindex}

  page_words, wccsizes = Combiner.CombineWords(allwords)

  if not os.path.exists(output_base):
    os.makedirs(output_base)


  foutbase = output_base + '/' + docid

  # Count wcc sizes
  fwcc = open(foutbase + '.wccsize', 'w')
  for size in sorted(wccsizes.keys()):
    print >>fwcc, str(size) + '\t' + str(wccsizes[size])
  fwcc.close()

  fcand = open(foutbase + '.cand', 'w')
  fcandfeat = open(foutbase + '.candfeature', 'w')
  fcandbox = open(foutbase + '.candbox', 'w')
  
  wordid = 0
  for pageid in page_words: 
    for word in page_words[pageid]:
      # pageid : [[cand1, cand2], [cand1, cand2, cand3]..]
      # '\t'.join([can[0], can[1].GetPrinted(), can[2].GetContent()])
      wordid += 1  # Start from 1!!!
      for candid in range(0, len(word)):
        cand = word[candid]

        ocrid = cand[0]
        candword = cand[2].GetContent()
        page = cand[1].GetPage()
        boxes = cand[1].GetBoxes()
        pos = cand[2].GetPOS()
        ner = cand[2].GetNER()
        lemma = cand[2].GetLemma()

        print >>fcand, '\t'.join([str(s) for s in [
          docid, wordid, candid, ocrid, candword
          ]])
        print >>fcandbox, '\t'.join([str(s) for s in [
          docid, wordid, candid, page] + boxes
          ])
        if ocrid == 'T':
          print >>fcandfeat, '\t'.join([str(s) for s in [
          docid, wordid, candid, pos, ner, lemma
          ]])

  print 'Total words:',wordid

  fcand.close()
  fcandfeat.close()
  fcandbox.close()






# Assume a fixed URL base.
# Output alignment results in output_base.*
def Align(urlbase, output_base, isDir=False, boxedCunei = False):

  tess_url = urlbase +'input.text'
  curlbase = urlbase + 'cuneiform-page-'
  curlend = '.html'

  print 'Loading Tesseract from:', tess_url
  if not isDir:
    twords = TessReader.ReadURL(tess_url)
  else:
    twords = TessReader.ReadPath(tess_url)
  # print 'Processing Tesseract...'

  flog = open(output_base + '.log', 'w')

  index = Combiner.BuildBoxIndexByPage(twords)
  succ_fail = [0, 0]

  # for (url, pagenum) in cunei_urls:

  # Assume a fixed cuneiform URL format.
  for pagenum in sorted(index.keys()):
    pagestr = '%04d' % pagenum
    url = curlbase + pagestr + curlend
    # print 'Loading Cuneiform Page', pagenum
    if not isDir:
      cchars = CuneiReader.ReadURL(url, pagenum)
    else:
      cchars = CuneiReader.ReadPath(url, pagenum)
    # print 'Processing Cuneiform Page', pagenum
    this_sc = Combiner.Combine(twords, cchars, index)
    for i in range(0,2): 
      succ_fail[i] += this_sc[i]
  
  # aligned, AGREED, miss_cuni, miss_tess
  stat = [0, 0, 0, succ_fail[1]]

  # print 'Printing results...'
  fout = open(output_base+'.diff.txt', 'w')
  for word in twords:
    linechar = ' '
    content = word.GetContent()
    alter = word.GetAlter()
    if alter == '':
      linechar = '.'
      stat[2] += 1
    elif content == alter:
      linechar = ' '
      stat[1] += 1
      stat[0] += 1
    else:
      linechar = 'X'
      stat[0] += 1
    print >>fout, '%s %20s %20s' % (linechar, word.GetContent(), word.GetAlter(), ), [b.GetPrinted() for b in word.GetBoxes()]
    # if word.GetAlter() == '':
    #   raw_input()
  fout.close()


  print >>flog, 'Alignment SUCC/Fail:', succ_fail
  print >>flog, 'STAT: aligned, AGREED, miss_cuni, miss_tess(wrong):'
  print >>flog, '\t'.join(['%5d %.4f' % (s, float(s)/len(twords)) for s in stat])
  print >>flog, 'Recall:', float(succ_fail[1]) / sum(succ_fail)

  flog.close()        

  fout = open(output_base+'.output.txt', 'w')
  lastsentence = 1
  wid = 1
  for word in twords: 
    sid = word.GetSentId()
    if sid != lastsentence:
      lastsentence = sid
      wid = 1
      print >>fout  # println

    # Word ID + all other parts
    print >>fout, '\t'.join([str(p) for p in 
      ([wid] + word.GetAllParts())
      ])
    wid += 1

  fout.close()


# Testing
if __name__ == "__main__": 
  if len(sys.argv) == 2:
    path = sys.argv[1]
    AlignBoxedFromPath([path], 'TEST_JOURNAL', './test')
  else:
    print 'Usage:',sys.argv[0],'<path>'
    sys.exit(1)
