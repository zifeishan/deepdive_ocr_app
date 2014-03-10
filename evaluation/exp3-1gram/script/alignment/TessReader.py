import re

from util import *
# from pyquery import PyQuery  # support url parsing
from struct import *

# def ReadURL(url):
#   trytime = 0
#   pq = None
#   while (trytime < 3):
#     try:
#       pq = PyQuery(url = url)
#       break
#     except:
#       print 'Timeout!', url
#       trytime += 1

#   if pq == None:
#     return Read('')

#   alltext = pq.text()
#   return Read(alltext)

def ReadPath(file_path):
  data = []
  fin = open(file_path)
  alltext = fin.read()
  return Read(alltext)

def Read(content):
  content = str(content)  # Encode in ascii
  PART_NUM = 9
  allwords = []
  lines = content.split('\n')
  # print len(lines), 'lines'
  
  for line in lines:
    # if line == '':
    #   break
    if line == '': # A Sentence
      continue
    parts = line.rstrip('\n').rstrip('\r').split('\t')

    if len(parts) != PART_NUM:
      print 'Content unrecognizable:', parts
      continue
      # id CONTENT POS1 POS2 STEM POS3 notsure notsure [page left top right bottum]
      # 1 Paleontological NNP O Paleontological nn  2 SENT_1  [p1l17t81r380b129],

    wid = parts[0]

    # print line
    # print parts
    # raw_input()
    word = NewWord(parts)

    allwords.append(word)
    # print word.GetContent(), len(word.GetBoxes())

    # TODO document/sent/word

  return allwords
