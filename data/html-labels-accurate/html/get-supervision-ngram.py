import codecs

import sys, os
from pyquery import PyQuery


path = '.'
outbase = 'output/'
if len(sys.argv) == 3:
  path = sys.argv[1]
  outbase = sys.argv[2]
else:
  print 'Usage:',sys.argv[0],'<path> <outbase>'
  sys.exit(1)

files = os.listdir(path)

for f in files:
  if not f.endswith('.html'): continue
  docid = f[:-len('.html')]
  print 'Processing', docid
  htmlpath = path + '/' + f
  html = open(htmlpath).read()
  pq = PyQuery(html)

  title = pq.find('.title')
  if title != None: 
    title = title.find('.cLink')
    if title != None:
      title = title.text()
  if title == None:
    title = ''

  text = pq.find('.page_fragment').text()
  words = text.split(' ')

  outpath = outbase + '/' + docid
  fout = codecs.open(outpath + '.seq', 'w', 'utf-8')
  for w in words:
    print >>fout, w
  # file.write(text)
  fout.close()

  for ngram in range(1, 4):
    grams = {}
    for i in range(0, len(words) - ngram + 1):
      thisgram = '\t'.join(words[i : i + ngram])
      if thisgram not in grams:
        grams[thisgram] = 0
      grams[thisgram] += 1

    outpath = outbase + '/' + docid
    fout = codecs.open(outpath + '.' + str(ngram) + 'gram', 'w', 'utf-8')
    for s in sorted(grams, key=grams.get, reverse=True):
      print >>fout, docid + '\t' + str(grams[s]) + '\t' + s
    fout.close()
