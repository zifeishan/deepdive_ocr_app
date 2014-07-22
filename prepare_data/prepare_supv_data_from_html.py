#! /usr/bin/python
# Sample usage: <this> <html_path> <outbase>
# NEW: ignore existing files in output dir

### Test with a single file:
# pypy prepare_supv_data_from_html.py eval /dfs/hulk/0/zifei/ocr/sd-html/JOURNAL_13652.html /tmp/
# pypy prepare_supv_data_from_html.py eval /dfs/hulk/0/zifei/ocr/sd-html/JOURNAL_72675.html /tmp/
# JOURNAL_72675: 

import codecs
import HTMLParser

htmlparser = HTMLParser.HTMLParser()

import sys, os
# from pyquery import PyQuery
# import BeautifulSoup
from BeautifulSoup import BeautifulSoup, Comment
import re

from HTMLParser import HTMLParser

# ( ) or (, , and )
# pa_remove_ref = r'(\( *\))|(\([^)]*(,|and)+[^)]*\))'
pa_remove_ref = r'\((and|,|;| )*\)'
# pa_remove_ref = r'\([^)]*\)'
# pa_remove_ref = r'(\( *\))|(\([^)a-zA-Z]*(,|and| )+[^)a-zA-Z]*\))'
re_remove_ref = re.compile(pa_remove_ref)

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
  print 'Got arguments:',sys.argv
  print 'Usage:',sys.argv[0],'<supv_or_eval> <path> <outbase>'
  print 'e.g. pypy ./prepare_supv_data_from_html.py supv ../data/html-labels-accurate/html/test-30docs/ ../data/test-supervision/'
  print 'e.g. pypy ./prepare_supv_data_from_html.py eval ../data/html-labels-accurate/html/test-30docs/ ../data/test-evaluation/'
  print 'Or run with a single HTML file:'
  print 'e.g. pypy ./prepare_supv_data_from_html.py eval ../data/html-labels-accurate/html/test-30docs/JOURNAL_13652.html ../data/test-evaluation/'
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

# is a single file!
if os.path.isfile(path): 
  # print 'Path',path,'is a single file!'
  files = [path]
  parts = path.rsplit('/', 1)
  if len(parts) > 1:
    path = parts[0]
  else:
    raise Exception('ERROR!!')

else:
  files = [path + '/' + f for f in os.listdir(path)]

for f in files:
  if not f.endswith('.html'): continue
  # Escape before and after
  docid = f[len(path) + 1 : -len('.html')]

  if os.path.exists(outbase + '/' + docid + '.seq_unsegmented'):
    print 'Skipping', docid
    continue

  print 'Processing', docid
  # htmlpath = path + '/' + f
  htmlpath = f
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

      # # Remove Resume section (not English)
      # if ESCAPE_FOR_EVAL and div.has_key('class') and 'svAbstract' in div['class']:
      #   divtitles = div.findAll('h2', {'class': 'secHeading'})
      #   for divtitle in divtitles:
      #     if 'R&eacute;sum&eacute;' in divtitle.text:
      #       print >>sys.stderr, '%s\tREMOVE RESUME:' % docid, div.text[:100],'...'
      #       div.extract()
      #       break

      # # Keep real abstracts
      # if 'class' in div:
      #   cls = div['class']
      #   if 'svAbstract' in cls and 'abstractHighlights' not in cls:
      #     continue
      #   else:
      #     print >>sys.stderr, '%s\tREMOVE DIV:' % docid, div.text[:100],'...'
      #     div.extract()
      # else:
      #   div.extract()

      if ESCAPE_FOR_EVAL and div.has_key('class') and \
        (
          'figTblUpiOuter' in div['class'] 
          # or 'btnHolder' in div['class']
          or 'refText' in div['class'] # ignore references
          or 'artFooterContent' in div['class']
        ):
        div.extract()  # Remove this div

      if ESCAPE_FOR_EVAL and div.has_key('class') and \
        ( 'abstractHighlights' in div['class'] # author highlights
          ):
        print >>sys.stderr, '%s\tREMOVE HIGHLIGHT:' % docid, div.text[:100],'...'
        div.extract()

      if ESCAPE_FOR_EVAL and div.has_key('class') and \
        ( 'formula' in div['class']
          ):
        print >>sys.stderr, '%s\tREMOVE FORMULA:' % docid, div.text[:100],'...'
        div.extract()

      # Remove Resume section (not English)
      if ESCAPE_FOR_EVAL and div.has_key('class') and 'svAbstract' in div['class']:
        divtitles = div.findAll('h2', {'class': 'secHeading'})
        for divtitle in divtitles:
          # if 'R&eacute;sum&eacute;' in divtitle.text:
          #   print >>sys.stderr, '%s\tREMOVE RESUME:' % docid, div.text[:100],'...'
          #   div.extract()
          if '&' in divtitle.text: # escape chars in title (French)
            print >>sys.stderr, '%s\tREMOVE OTHER LANGUAGE:' % docid, div.text[:100],'...'
            div.extract()

    # Remove copyright
    divs = frag('p')
    for div in divs:
      # if ESCAPE_FOR_EVAL:
      #   if not div.has_key('class') or ('section' not in div['class'] and 'articleText' not in div['class']):
      #     print >>sys.stderr, '%s\tREMOVE PARA:' % docid, div.text[:100],'...'
      #     div.extract()
      if ESCAPE_FOR_EVAL and div.has_key('class') and \
        (
          'copyright' in div['class'] 
        ):  # ignore copyright
        div.extract()  # Remove this div

      else:  # a valid paragraph
        intra_refs = div.findAll('a', {'class': 'intra_ref'})
        for ref in intra_refs:
          # print >>sys.stderr, 'Remove ref:', ref.text
          ref.extract()


    # Remove keyword headline (e.g. Keywords / Mots cl\xc3s)
    divs = frag('h2')
    for div in divs:
      # if ESCAPE_FOR_EVAL:
      #   if not div.has_key('class') or 'svArticle' not in div['class']:
      #     print >>sys.stderr, '%s\tREMOVE H2:' % docid, div.text[:100],'...'
      #     div.extract()

      if ESCAPE_FOR_EVAL and div.has_key('id') and \
        (
          'kwd_' in div['id'] 
        ):  # ignore copyright
        print >>sys.stderr, '%s\tREMOVE KW TITLE:' % docid, div.text[:100],'...'
        div.extract()  # Remove this div

    # Remove keyword list
    divs = frag('ul')
    for div in divs:
      if ESCAPE_FOR_EVAL and div.has_key('class') and \
        (
          'keyword' in div['class']
        ):  # ignore copyright
        print >>sys.stderr, '%s\tREMOVE KW LIST:' % docid, div.text[:100],'...'
        div.extract()  # Remove this div


    # ##### New simpler filter: (DOES NOT WORK)
    # if ESCAPE_FOR_EVAL:
    #   for anything in frag:
    #     if anything.has_key('class'):
    #       if 'section' in anything['class']:
    #         continue
    #       if 'articleText' in anything['class']:
    #         continue
    #       if 'abstract' in anything['class'] and \
    #         'abstractHighlights' not in anything['class']:
    #         continue

    #     print 'Extracting:', anything.text[:80]
    #     anything.extract()  # remove this thing



    fragtext = frag.findAll(text=True)
    visible_texts = filter(visible, fragtext)

    thistext = ' '.join(visible_texts) + ' '
    thistext = htmlparser.unescape(thistext)  # Decode
    thistext = re.sub('\xa0', ' ', thistext)  # HTML space
    thistext = re.sub(' +', ' ', thistext)  # Multiple spaces to only one
    thistext = re.sub('\xe2\x80\x93', '-', thistext) # 'super -' -> '-'

    thistext = re.sub('\xe2\x80\x94', '-', thistext) # 'super -' -> '-'
    thistext = re.sub('\xe2\x88\x92', '-', thistext)
    thistext = re.sub('\xe2\x80\x9d', '"', thistext) # "
    thistext = re.sub('\xe2\x80\x9c', '"', thistext)
    text += thistext

    # print >>sys.stderr, thistext
    # Remove references: (...4 numbers / et al...)
    # print >>sys.stderr, re.findall(re_remove_ref, thistext)
    # thistext = re.sub(re_remove_ref, '', thistext)

    # text += '\n'  # between each fragment

  # text = pq.find('.page_fragment').text()
  # words = text.split(' ')


  text = re.sub(re_remove_ref, '', text)

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
