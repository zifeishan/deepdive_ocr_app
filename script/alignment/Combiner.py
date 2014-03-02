from util import *
import re
import snap  # Calc Connected Components
import sys

# Return a index of each page: index{1:[(b1,w1), (b2,w2)...], 2:[b10,b11..]}
# The list is sorted by Box comparator.
# If one word contains multiple boxes, they will be ALL indexed to the SAME word object.

# CHANGE: If one word contains multiple boxes, they will be ONLY indexed into the FIRST word object.

# TODO: do not do either: find someway better!!
def BuildBoxIndexByPage(words):
  index = {}
  for w in words:
    boxes = w.GetBoxes()
    for b in boxes:
      p = b.GetPage()
      if p not in index:
        index[p] = []
      index[p].append((b, w))  # page P, add a pair: box B, word W
      break

  # for p in index:
  #   index[p].sort() # Sort the list for every page, based on box ULRD.

  return index

def GetNextSub(sub, maxsub):
  sub = sub + 1
  if sub >= maxsub:
    sub = 0
  return sub


def IsSingleMark(string):
  if len(string) != 1:
    return False
  return re.match("^[A-Za-z0-9]*$", string)  # Anything but letters and chars


NO_ORDER_MARK = None
# x, y: tuples
# If higher-dim is None, use lower-dim to sort
def order_compare(x, y):
  for i in range(0, len(x)):
    if x[i] == NO_ORDER_MARK or y[i] == NO_ORDER_MARK:
      # neglect, use low-dim
      continue
    elif x[i] != y[i]:
      return x[i] - y[i]  # - for x<y, + for x>y
    else:   # x[i] == y[i]
      continue

  return 0  # cannot compare with all dimensions



# Combine words based on box overlaps!
# allwords: {ocrid: words}. e.g. {'T': twordsindex, 'C': cwordsindex}
# RETURN:
#   pageid : [[cand1, cand2], [cand1, cand2, cand3]..]
#   cand*: (ocrid, box, word)
#   e.g. 
#   for can in word:
#     print '\t'.join([can[0], can[1].GetPrinted(), can[2].GetContent()])
def CombineWords(allwords, orderby = ['T', 'C']):
  page_cands = {}  # pageid : [OCRwords]
  page_words = {}  # pageid : [[cand1, cand2], [cand1, cand2, cand3]..]
  # where
  page_cands_order = {}  # ocrid : pageid : cand_sub : ori_ocr_order  (inverted index, only for "orderby" ocrs)
  for ocrid in allwords:
    index = allwords[ocrid]
    page_cands_order[ocrid] = {}
    for pageid in index:
      if pageid not in page_cands: 
        page_cands[pageid] = []
      if pageid not in page_cands_order[ocrid]:
        page_cands_order[ocrid][pageid] = {}

      for ocr_sub in range(0, len(index[pageid])):
        pair = index[pageid][ocr_sub]
        box = pair[0]
        word = pair[1]
        # New: handle C bad outputs
        if box.GetLeft() == 0 and box.GetUp() == 0 and ocrid == 'C':
          print >>sys.stderr, box.GetPrinted(), word.GetContent()
          continue  # Ignore this candidate

        page_cands[pageid].append( (ocrid,) + pair )  # (ocrid, box, word)

        # if ocrid == orderby:  # slow... TODO
        cand_sub = len(page_cands[pageid]) - 1
        page_cands_order[ocrid][pageid][cand_sub] = ocr_sub
        # print page_cands_order
        # raw_input()

  wccsizes = {}
  for pageid in page_cands:
    nodes = page_cands[pageid]  # [(ocrid, box, word), ...]
    graph = snap.PUNGraph.New()   # Undirected graph
    for i in range(0, len(nodes)):
      _ret = graph.AddNode(i)

    # Add overlapping edges in undirected graph
    for i in range(0, len(nodes)):
      for j in range(i + 1, len(nodes)):
        b1 = nodes[i][1]
        b2 = nodes[j][1]
        if b1.IsOverlapSamePage(b2):
          graph.AddEdge(i, j)

    # TODO After aggregate by WCCs, we need a proper order.
    # Now picking order by first word in Tesseract Order! 
    # If not appearing in Tesseract, pick order as Cuneiform order. (how?) or neglect???

    words = []  # candidates separated: [ [order, [cand1, cand2]], [order, [cand1]], ...]
    wccs = snap.TCnComV()
    snap.GetWccs(graph, wccs)
    order_comp = {}

    for comp in wccs:
      wccsz = comp.Len()
      if wccsz not in wccsizes:
        wccsizes[wccsz] = 0
      wccsizes[wccsz] += 1

      # print "Size of component: %d" % comp.Len()
      # for arr in [[nodes[nid][0], nodes[nid][1].GetPrinted(), nodes[nid][2].GetContent()] for nid in comp]:
      #   print ' ', '\t'.join(arr)

      this_cc = [nodes[nid] for nid in comp]
      this_order = [NO_ORDER_MARK] * len(orderby)
      for nid in comp:
        ocrid = nodes[nid][0]
        ocrorder = page_cands_order[ocrid][pageid][nid]
        if ocrid in orderby:
          i = orderby.index(ocrid)
          if this_order[i] == NO_ORDER_MARK or this_order[i] > ocrorder:
            this_order[i] = ocrorder

      # else:
      #   words.append( (this_order, [nodes[nid] for nid in comp]) )  
      words.append( (this_order, [nodes[nid] for nid in comp]) )
      # raw_input()

    words.sort(cmp=order_compare, key=lambda word: word[0])

    # print 'Top 100 Orders:', [w[0] for w in words][:100]
    # print 'None Orders:'
    # for l in [
    #   [w[0]
    #     # +[w[1][0][2].GetContent()]
    #     for w in words[i - 3 : i + 3]] 
    #   for i in range(3, len(words) - 3) 
    #   if None in words[i][0]
    # ]:
    #   print l


    # Test case: 
    # python alignment/Align.py /Users/Robin/Documents/repos/deepdive_ocr/deepdive_danny/app/ocr/data/html-labels-accurate/data-labeled/ocroutput/JOURNAL_28971.pdf.task/
    # [7, 6], [8, 7], [9, 9], [12, 13], [13, 10], [14, None], [15, None], [16, None], [17, None], [18, None]
    # [19, None], ... , [94, None]
    # [95, None], [96, None], [97, None], [98, None], [None, 14], [None, 15], [99, 16], [102, 17], [104, 18], [105, 19]


    test_orders = [w[0] for w in words]
    words = [w[1] for w in words]  # remove order
    for i in range(len(words)):
      word = words[i]
      order = test_orders[i]
  
      # if order[0] == None:  
      #   print 'Order:', order
      #   print len(word), 'candidates...'
      #   for can in word:
      #     print '\t'.join([can[0], can[1].GetPrinted(), can[2].GetContent()])
      #   # if len(word) != 2 or len(word) >= 2 and word[0][2].GetContent() != word[1][2].GetContent():
      #   #   raw_input()
      #   if len(word) == 1:
      #     raw_input()

    page_words[pageid] = words

  return page_words, wccsizes 




# combine cchars into twords, stored in "Word" object!
def Combine(twords, cchars, index=None):
  if index == None:
    index = BuildBoxIndexByPage(twords)

  page = -1  # assume cchars are all in a same page (no problem if not)
  maxsub = 0
  last_sub = 0  # Start from sub 0

  succ_fail = [0, 0]
  # Try to align each character to a box.
  for char in cchars:

    # Suppose there is only ONE box for the character
    mybox = char.GetBoxes()[0]

    tpage = mybox.GetPage()
    if tpage != page: 
      page = tpage
      maxsub = len(index[page])
      last_sub = 0
      # print 'Processing Page:', page

    isStarting = False
    sub = last_sub

    aligned = False
    
    while sub != last_sub or isStarting == False:
      isStarting = True
      pair = index[page][sub] 
      box = pair[0]
      word = pair[1]
      if box.Contain(mybox):  # char is contained in this box

        # Special case: 
        # Words and marks can have SAME box in Tesseract.
        # Therefore it is very hard to align.
        # We assume in this case they are close to each other, and 
        nextsub = GetNextSub(sub, maxsub)
        nextbox = index[page][nextsub][0]
        nextword = index[page][nextsub][1]

        # Assume that one word has at most 2 boxes. 
        # There is a case that [b1,b2] [b1,b2] are continuous
        # e.g.
        # X                    (          (Cam-bridge ['P12,1919 2474 1984 2501', 'P12,1410 2506 1475 2532']
        # .            Cambridge                      ['P12,1919 2474 1984 2501', 'P12,1410 2506 1475 2532']
        if not nextbox.Equal(box):  # Try the next-next one
          nnsub = GetNextSub(nextsub, maxsub)
          nnbox = index[page][nnsub][0]
          nnword = index[page][nnsub][1]
          if nnbox.Equal(box):
            nextsub = nnsub
            nextbox = nnbox
            nextword = nnword

        if nextbox.Equal(box): # same box, the case might happen
          accumulated = word.GetAlter()
          wordtext = word.GetContent()

          # Case 1: exact match already
          # Case 2: equal length, non-alphabet left, next same.
          # VERY-LOOSE match: as long as LENGTH are equal!
          # assumption: they will NOT neglect characters.
          if (wordtext == accumulated) or (\
            len(wordtext) == len(accumulated) 
            # and nextword.GetContent() == char.GetContent() 
            # and IsSingleMark(char.GetContent())
            ):
            # Match to next word!
            sub = nextsub
            word = nextword
          # else nothing happens, still match to this word

        word.AddAlterChar(char.GetContent())
        aligned = True
        break

      # Not match, next sub.
      sub = GetNextSub(sub, maxsub)

    last_sub = sub  # update to the latest sub found. 
    # Worst case: O(n) for each iteration, 
    # n is number of words in a document.


    if not aligned:
      # print 'Fail to align char:', char.GetContent(), mybox.GetBoxes(), 'P:', page
      # print 'Last Word aligned:', index[page][last_sub][1].GetContent()
      # raw_input()
      succ_fail[1] += 1
    else:
      succ_fail[0] += 1

  return succ_fail

