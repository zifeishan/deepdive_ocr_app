#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import os,sys   # needed by most
import urllib
from pyquery import PyQuery  # support url parsing
import re
from util import *
import pickle, json
import shutil

g_dict = {}
g_path = 'web_occur_dict.json'
g_path_backup = 'web_occur_dict-backup.json'
g_counter = 0

def ReadDict(path = g_path):
  global g_dict
  try:
    fin = open(path, 'r')
  except IOError:
    return
  g_dict = json.load(fin)  # global dict
  print 'Loaded Dictionary of size:', len(g_dict)

def WriteDict(path = g_path):
  global g_dict
  print 'Copying Dictionary file:'
  try:
    shutil.copyfile(path, g_path_backup)
  except IOError:
    x = 1
  fout = open(path, 'w')
  json.dump(g_dict, fout, indent=1)
  fout.close()
  print 'Dictionary saved to:', path

def Transform(word):
  ori = word
  word = Strip(word)
  word = word.replace(' ', '+')
  word = re.sub(r"[^a-zA-Z0-9\-+\.]", "", word)
  # print ori, word
  return word

def Occur(word):
  global g_dict

  word = Transform(word)

  if word in g_dict:
    # print 'Found!', word, g_dict[word]
    return math.log(g_dict[word] + 1)

  # url = 'http://www.google.com/search?q='+word
  url = 'http://www.bing.com/search?q=%2b'+word
  # +'&filters=rcrse%3a"1"&FORM=RCRE'
  # print url
  
  try:
    pq = PyQueryTimeOutRetry(url = url, retry = 3)
  except TimeoutError:
    print 'Timeout!', word
    return 0

  counts = pq.find('.sb_count')
  if counts == None or counts.text() == None:
    count = 0
    g_dict[word] = count
    return math.log(count + 1)

  try:
    count = int(counts.text().rstrip(' results').replace(',', ''))
  except Error:
    print 'Error:', x.text()
    count = 0
  
  global g_counter
  g_counter += 1

  if g_counter % 30 == 0:
    WriteDict(g_path)

  g_dict[word] = count
  return math.log(count + 1)



  # spells = pq.find('#sp_requery')
  # # spells = pq('a').filter('#sp_requery')
  # print spells

if __name__ == "__main__": 
  print Occur('asoif3ohf293fhdfh')
  print Occur('gibbs sampling')

# word = Transform(word)
# # url = 'http://www.google.com/search?q='+word
# url = 'http://www.bing.com/search?q=%%2b'+word
#     # +'&filters=rcrse%%3a"1"&FORM=RCRE'
# print url
# pq = PyQuery(url = url)
# pq = PyQuery(url = 'http://www.bing.com/search?q=barark+obama/')

# counts = pq('div').filter('.sb_count')
# print counts

# spells = pq('a').filter('#sp_requery')
# print spells
