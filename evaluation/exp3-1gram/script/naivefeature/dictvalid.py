from util import *
import enchant
dictionary = enchant.Dict("en_US")

def DictValid(word):
  # word = word.strip('.,?!;')
  word = Strip(word)
  if len(word) == 0:
    return 0
  if dictionary.check(word): # word exists
    return 1
  else:
    return 0
