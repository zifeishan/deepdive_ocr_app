#! /usr/bin/python
# Sample usage: <this> <html_path> <outbase>

import codecs

import sys, os
# from pyquery import PyQuery
import BeautifulSoup
import re

from HTMLParser import HTMLParser


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


SEGMENT_CMD = 'CLASSPATH=../util/stanford-parser.jar java edu.stanford.nlp.process.PTBTokenizer'

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
  # pq = PyQuery(html)
  soup = BeautifulSoup.BeautifulSoup(html)

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
  # text += '\n'
  # soup.find('page_fragment').text
  allfrags = soup.findAll('div', {'class': 'page_fragment'})
  for frag in allfrags:
    fragtext = frag.findAll(text=True)
    visible_texts = filter(visible, fragtext)
    text += ' '.join(visible_texts) + ' '
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
  print '-- Done, saved to',outpath + '.seq'

  words = text.split(' ')
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
