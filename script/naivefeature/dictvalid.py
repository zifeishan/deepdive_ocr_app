from util import *
# import enchant
# dictionary = enchant.Dict("en_US")

DICT_FILE = '/usr/share/dict/words'

dict_en = set([l.strip() for l in open(DICT_FILE).readlines()])

def DictValid(word):
  # word = word.strip('.,?!;')
  word = Strip(word)
  if len(word) == 0:
    return 0
  # if dictionary.check(word): # word exists
  if word in dict_en:
    return 1
  else:
    return 0
