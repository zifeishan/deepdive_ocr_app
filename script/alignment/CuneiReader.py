from util import *
from pyquery import PyQuery  # support url parsing
from struct import *
import sys

def ReadURL(url, pageid = 1):
  trytime = 0
  pq = None
  while (trytime < 3):
    try:
      pq = PyQuery(url = url)
      break
    except KeyboardInterrupt:
      raise KeyboardInterrupt
    except:
      print 'Timeout!', url
      trytime += 1

  if pq == None:
    return Read(None)

  return Read(pq, pageid)

def ReadPath(file_path, pageid = 1):
  data = []
  fin = open(file_path)
  alltext = fin.read()
  pq = PyQuery(alltext)
  return Read(pq, pageid)


def Read(query, pageid = 1):
  allwords = []
  if query == None:
    return allwords

  pq = query
  lines = pq.find('.ocr_line')
  ids = []
  for l in lines:
    lid = l.get('id')
    if lid != None:
      ids.append(lid)
  # print ids
  # raw_input()

  # Iterate on each line
  for lid in ids:
    line = pq.find('.ocr_line#'+lid)
    text = line.text()
    # try:
    #   text = str(line.text())
    # except UnicodeEncodeError:
    #   print 'Cannot Encode:',line.text()
    #   continue

    if text == '':
      # print 'Empty line.', lid
      continue
    boxes = line.find('.ocr_cinfo')
    # print lid, boxes

    if len(boxes) == 0:
      print 'Warning: Empty box', lid, text
      continue
    if len(boxes) > 1:
      print 'Error: multiple boxes in line', text

    bs = boxes[0].get('title')
    if bs != None and bs.startswith('x_bboxes'):
      parts = bs.lstrip('x_bboxes ').strip().split(' ')
      # print lid, len(parts) / 4, len(text)  # Should be integer
      # print len(text)         # should be above (- 1), last space 

    if not len(parts)/ 4 == len(text) and not len(parts) / 4== len(text) + 1:
      print 'Warning: #box not right', len(parts), len(text)

    # words, subs = WordSplitter(text)

    # Generate a word for each character, return them, then combined with another side!
    for i in range(0, len(text)):
      c = text[i]
      boxes = parts[i * 4 : i * 4 + 4]
      w = Word()
      b = Box()
      b.SetBoxes(boxes)
      b.SetPage(pageid)

      # Only jump this letter if empty box
      if b.IsEmpty():
        continue
      w.AddBox(b)

      try:
        c = str(c)
      except UnicodeEncodeError:
        # print 'Cannot encode character:', c, b.GetPrinted(), 'P:', pageid
        c = '?'      

      w.SetContent(c)
      allwords.append(w)

    # Finish this line

  # Finish all lines
  return allwords
