CTYPE = 'ct'
PAGE = 'p'
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
CONTENT = 'c'
BOX = 'b' 

POS1 = 'P1'
POS2 = 'P2'
STEM = 'st'
POS3 = 'P3'

SURE_ORI = 'SO'
UNSURE_ORI = 'UO'
SURE_SUGG = 'SS'
UNSURE_SUGG = 'US'

# import enchant
# dictionary = enchant.Dict("en_US")
import re
strip_pattern = re.compile('\W')


def BoxEmpty(box):
  return box[LEFT] == box[RIGHT] or box[UP] == box[DOWN]

def BoxContain(box1, box2):
  return box1[LEFT] <= box2[LEFT] + BOX_THRESHOLD \
    and box1[UP] <= box2[UP] + BOX_THRESHOLD \
    and box1[DOWN] >= box2[DOWN] - BOX_THRESHOLD \
    and box1[RIGHT] >= box2[RIGHT] - BOX_THRESHOLD \
    and box1[PAGE] == box2[PAGE]
    # Assume a box only has one page..

def BoxAbove(box1, box2):
  return (box1[DOWN] < box2[UP] + BOX_THRESHOLD and box1[PAGE] == box2[PAGE])\
    or box1[PAGE] < box2[PAGE]

def BoxLeft(box1, box2):
  return (box1[RIGHT] < box2[LEFT] + BOX_THRESHOLD and box1[PAGE] == box2[PAGE])\
    or box1[PAGE] < box2[PAGE]

def BoxEqual(box1, box2):
  return BoxContain(box1, box2) and BoxContain(box2, box1)

def BoxBefore(box1, box2):
  # if box1[PAGE] < box2[PAGE]:
  #   return True
  # if box1[PAGE] > box2[PAGE]:
  #   return False
  # if box1[DOWN] < box2[UP] + BOX_THRESHOLD and\
  #    box1[RIGHT] < box2[LEFT] + BOX_THRESHOLD:
  #    return True
  # if box2[DOWN] < box1[UP] + BOX_THRESHOLD and\
  #    box2[RIGHT] < box1[LEFT] + BOX_THRESHOLD:
  #    return False
  # # Else: Not sure whether left or above is top-priority

  if box1[PAGE] < box2[PAGE]:
    return True
  if box1[PAGE] > box2[PAGE]:
    return False
  # Same page: TODO now prioritize ABOVE than LEFT
  if box1[DOWN] < box2[UP] + BOX_THRESHOLD:
    return True
  elif box1[UP] <= box2[UP] + BOX_THRESHOLD \
    and box1[DOWN] >= box2[DOWN] - BOX_THRESHOLD:
    if box1[RIGHT] < box2[LEFT] + BOX_THRESHOLD:
      return True
  return False

def Print(word):
  ret = '\t'.join([
    '%20s' % word[CONTENT], 
    str(word[BOX][PAGE]), 
    str(word[BOX][LEFT]), 
    str(word[BOX][UP]),
    str(word[BOX][RIGHT]),
    str(word[BOX][DOWN])
    ])
  print ret

# Check spell in alterlist.
def SpellCheck(alterlist, dictionary):
  validlist = []
  for word in alterlist:
    word = Strip(word)
    if len(word) == 0:
      continue
    if dictionary.check(word): # word exists
      validlist.append(word)
  if len(validlist) == 1:
    return validlist[0], SURE_ORI
  elif len(validlist) > 1:
    return validlist, UNSURE_ORI
  # len(validlist) == 0:
  else:
    inter = set(dictionary.suggest(alterlist[0]))
    union = set(dictionary.suggest(alterlist[0]))
    for i in range(1, len(alterlist)):
      newl = dictionary.suggest(word)
      inter = inter.intersection(newl)
      union = union.union(newl)
    if len(inter) == 1:
      return inter.pop(), SURE_SUGG
    elif len(inter) > 1:
      return inter, UNSURE_SUGG
    else:
      return union, UNSURE_SUGG

# TODO only pick first on suggestion list. hard to get right
# Only suggest 1 word for each option
def GetSuggestions(options):
  suggs = []
  for word in options:
    word = Strip(word)
    if len(word) == 0:
      suggs.append('')
      continue
    slist = dictionary.suggest(word)
    if len(slist) != 0:
      suggs.append(slist[0])
    else: 
      suggs.append('')
  return suggs

def Strip(word):
  # return word.strip('.,?!;:')
  return re.sub(strip_pattern, '', word)
  # print string