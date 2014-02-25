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
  # PART_NUM = 7
  # data = []
  content = str(content)  # Encode in ascii
  PART_NUM = 7
  allwords = []
  lines = content.split('\n')
  
  for line in lines:
    if line == '':
      continue
    parts = line.rstrip('\n').rstrip('\r').split('\t')
    # word = {}

    if len(parts) != PART_NUM:
      print 'Content unrecognizable:', parts
      continue

    word = NewCuneiWord(parts)
    if word.GetContent() != '':
      allwords.append(word)
      # if 'SPECFONT' in parts[0]:
      #   print word.GetAllParts()

  return allwords
