#! /usr/bin/python
# Sample usage: <this> <html_path> <outbase>
# NEW: ignore existing files in output dir

import codecs

import sys, os
# from pyquery import PyQuery
# import BeautifulSoup
from BeautifulSoup import BeautifulSoup, Comment
import re

from HTMLParser import HTMLParser


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


SEGMENT_CMD = 'CLASSPATH=../util/stanford-parser.jar java edu.stanford.nlp.process.PTBTokenizer -options "ptb3Escaping=false" '

path = '.'
outbase = 'output/'
if len(sys.argv) == 4:
  supv_or_eval = sys.argv[1]
  path = sys.argv[2]
  outbase = sys.argv[3]
else:
  print 'Usage:',sys.argv[0],'<supv_or_eval> <path> <outbase>'
  print 'e.g. pypy ./prepare_supv_data_from_html.py supv ../data/html-labels-accurate/html/test-30docs/ ../data/test-supervision/'
  print 'e.g. pypy ./prepare_supv_data_from_html.py eval ../data/html-labels-accurate/html/test-30docs/ ../data/test-evaluation/'
  sys.exit(1)

# Parse whether escape References / figures / tables for evaluation
ESCAPE_FOR_EVAL = False
if 'supv' in supv_or_eval:
  ESCAPE_FOR_EVAL = False
elif 'eval' in supv_or_eval:
  ESCAPE_FOR_EVAL = True
else:
  print 'Error parsing supv / eval argument.'
  sys.exit(1)


if not os.path.exists(outbase):
  os.makedirs(outbase)

files = os.listdir(path)

for f in files:
  if not f.endswith('.html'): continue
  docid = f[:-len('.html')]

  if os.path.exists(outbase + '/' + docid + '.seq_unsegmented'):
    print 'Skipping', docid
    continue

  print 'Processing', docid
  htmlpath = path + '/' + f
  html = open(htmlpath).read()
  html = re.sub('\&lt;', '<', html)
  html = re.sub('\&gt;', '>', html)
  html = re.sub('&nbsp;', ' ', html)  # handle html non-breaking spaces

  # pq = PyQuery(html)
  soup = BeautifulSoup(html)

  # Remove comments
  comments = soup.findAll(text=lambda text:isinstance(text, Comment))
  [comment.extract() for comment in comments]

  # title = pq.find('.title')
  # if title != None: 
  #   title = title.find('.cLink')
  #   if title != None:
  #     title = title.text()
  # if title == None:
  #   title = ''
  title = soup.find('title')  # TODO
  if title != None: 
    if title.find('cLink') != None:
      title = title.find('cLink').text
    else:
      title = title.text
  if title == None:
    title = ''

  text = title + ' '
  allfrags = soup.findAll('div', {'class': 'page_fragment'})
  for frag in allfrags:
    # Filter figures and tables and references
    divs = frag('div')
    for div in divs:
      if ESCAPE_FOR_EVAL and div.has_key('class') and ('figTblUpiOuter' in div['class'] 
        # or 'btnHolder' in div['class']
        or 'refText' in div['class']):  # ignore references
        div.extract()

    fragtext = frag.findAll(text=True)
    visible_texts = filter(visible, fragtext)
    text += ' '.join(visible_texts) + ' '
    text = re.sub(' +', ' ', text)  # Multiple spaces to only one

    # text += '\n'  # between each fragment

  # text = pq.find('.page_fragment').text()
  # words = text.split(' ')

  outpath = outbase + '/' + docid
  fout = codecs.open(outpath + '.seq_unsegmented', 'w', 'utf-8')
  # for w in words:
  #   print >>fout, w
  print >>fout, text
  fout.close()

  print '-- Segment on',outpath + '.seq_unsegmented'
  os.system(SEGMENT_CMD + ' <' + outpath + '.seq_unsegmented >'
    + outpath + '.seq')
  print '-- Done, saved to', outpath + '.seq'


  words = [l.rstrip('\n') for l in codecs.open(outpath + '.seq', 'r', 'utf-8').readlines()]

  print len(words), 'words parsed.'

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
