#!/usr/bin/python
# -*- coding: utf-8 -*-

# This one extract labels from Zifei's labeled files (rules & labels)
# Just extract labels.
# It is Wordy, non-optimized.

import sys, re
import pprint
import itertools
pp = pprint.PrettyPrinter(indent=2) # pretty printer


class ResultLine:
  def __init__(self):
    self.wid = 0
    self.numwords = 0
    self.tcorr = False
    self.ccorr = False
    self.rules = []  # arrays of Sets.
    self.actualwords = []

def TCPrinter(arr, stream):
  print >>stream, '  Tesseract:', arr[0]
  print >>stream, '  Cuneiform:', arr[1]

def ParseRuleComb(rulecomb, tags):
  s = sorted(rulecomb.split('+'))
  for tag in s:
    if tag not in tags:
      print 'WARNING: unknown tag:', tag, 'in',rulecomb
      s.remove(tag)
  return tuple(s)

def EncodeRuleComb(ruletuple):
  return '+'.join(ruletuple)


# 
def MyLabelExtract(labeled_file, ocr_file):

  path = labeled_file
  ocrpath = ocr_file

  lines = [l.strip(' \n') for l in open(path).readlines()]
  ocrlines = [l.strip('\n') for l in open(ocrpath).readlines()]

  tot_doc = 0       # For recall
  diff_doc = 0      # For recall on disagreed outputs
  tot_ocr = [0, 0]  # For acc
  non_correct = 0   # Both OCR fails
  correct = [0, 0]  # OCR results
  diff_correct = [0, 0]  # OCR results on disagreed words
  solved = 0        # If apply all rules, how many correct answers recalled

  tags = sorted(['twchar', 'cwchar', 'upp', 'charuni', 'comb', 'url', 'dot', 'upper', 'ocrdocacc', 'statc', 'statcgram', 'sw', 'swgram', 'stats', 'd', 'pos', 'posgram', 'ner', 'number', 'persondot', 'by', 'etal', 'lemma', 'path', 'kbe', 'kbr', 'ed', 'edrule', 'seg', 'rmchar', 'numconf'])
  
  # This map gives an UPPER BOUND for: only using this rule, how many correct answers recalled
  know_tot = {t:0 for t in tags}  

  # This map gives an UPPER BOUND for: only using this rule, how many correct answers out of the DISAGREED 
  know_disagree = {t:0 for t in tags}  

  # This map gives an UPPER BOUND for: only using this rule, how many correct answers out of the DISAGREED 
  know_noncorrect = {t:0 for t in tags}  

  # This is a dict: for each knowledge, if removed, how many words are lost. (recall lost)
  tag_lesion = {t:0 for t in tags}

  # Array of ResultLine instances
  reslines = []

  # docid = ''
  # if ocrpath.endswith('.output.txt'):
  #   docid = ocrpath[:-len('.output.txt')]
  # else:
  #   print 'FATAL: Wrong ocrpath. Cannot parse docid!'
  #   sys.exit(1)
  
  wid = -1

  for lineid in range(0, len(lines)):
    thisl = lines[lineid]
    l = thisl

    if l == '':  # empty line
      continue

    wid += 1

    if '///' in l:
      l = l.replace('///', '|||')

    # Improve with OCR files!!
    # w11 = l[3:18].strip(' ')   # TODO: what if too long?
    # w22 = l[19:19+15].strip(' ')
    ocrparts = ocrlines[lineid].split('\t')
    w1 = ocrparts[1]
    w2 = ocrparts[2]
    # if w1 != w11 or w2 != w22:
    #   print w1, w11, w2, w22


    l = l.split('|||')
    # print l

    if len(l) < 2:  # agreed and correct
      tot_doc += 1
      for i in (0,1):
        tot_ocr[i] += 1
        correct[i] += 1
      for sol in know_tot: 
        know_tot[sol] += 1  # all solutions can solve it

      # AppendNewLine
      rsline = ResultLine()
      rsline.wid = wid
      rsline.tcorr = True
      rsline.ccorr = True
      rsline.numwords = 1
      rsline.actualwords = [w1]
      # rsline.answers = ['1', '2']
      reslines.append(rsline)

      continue

    args = [p.strip(' ') for p in l[1].split('$')]
    # sol_str = [s.strip() for s in args[0].split(',')]
    sol_str = args[0]
    answers = args[1:]

    if len(answers) == 0:  # no mark, ignore this word.
      print 'NOMARK:', l
      continue

    # Count this word.
    if w1 != '': 
      tot_ocr[0] += 1
    if w2 != '': 
      tot_ocr[1] += 1

    this_num = 0
    if len(answers) == 1 and answers[0] == '':  # this is not a word, no recall
      this_num = 0
    else:
      this_num = len(answers)

    tot_doc += this_num
    diff_doc += this_num

    this_non_correct = False

    if answers[0] == '1':  # T correct
      correct[0] += this_num
      diff_correct[0] += this_num
    elif answers[0] == '2':  # C correct
      correct[1] += this_num
      diff_correct[1] += this_num
    else:
      non_correct += this_num
      this_non_correct = True

    if w2 == '' and sol_str == '' and answers[0] in ['', '1']:  # auto-pick...
      # print 'DSW:',thisl
      sol_str = 'd,sw'
    # ASSUMPTION: IF ONLY ONE HAS OUTPUT, it should be trivial to get $1 or $ right.
    # JUST USE d + sw for all of them.

    # print 'Solutions:',sol_str,'\tAnswers:',answers

    # examine solutions
    sols = [p.strip(' ') for p in sol_str.split(',') if p.strip(' ') != '']

    if '?' in sol_str:  # cannot be solved with automatic knowledge
      sols = []           # no solutions

    if len(sols) > 0:  # solvable
      solved += this_num

    # Create a result line and store.
    rsline = ResultLine()
    sets = [{s for s in ParseRuleComb(s, tags)} for s in sols if len(ParseRuleComb(s, tags)) > 0]
    # if sets == []: print thisl
    rsline.wid = wid
    rsline.rules = sets # Sets
    rsline.tcorr = (answers[0] == '1')
    rsline.ccorr = (answers[0] == '2')
    rsline.numwords = this_num
    rsline.actualwords = answers
    if answers[0] == '1':
      rsline.actualwords = [w1]
    elif answers[0] == '2':
      rsline.actualwords = [w2]

    reslines.append(rsline)

    for sol in sols:
      if sol not in know_tot:
        if sol == '': continue
        # print sol
        unknown = False
        comb = ParseRuleComb(sol, tags)  # May be a combination. tuple of the combination.
        # print comb
        for k in comb:
          if k not in know_tot:
            unknown = True
        
        if unknown:
          continue
        else:
          sol = EncodeRuleComb(comb)
          know_tot[sol] = 0
          know_disagree[sol] = 0
          know_noncorrect[sol] = 0

      know_tot[sol] += this_num
      know_disagree[sol] += this_num
      if this_non_correct:
        know_noncorrect[sol] += this_num

  # print 'TOTAL WORDS:', sum([l.numwords for l in reslines]) # agreed

  classes = {}  # For return to table extraction
  corrections = {}
  for rsline in reslines:
    # print rsline.wid, rsline.actualwords

    wid = rsline.wid
    corrected = ' '.join(rsline.actualwords)
    if rsline.tcorr and rsline.ccorr: 
      classchar = '0'
    elif rsline.tcorr: 
      classchar = 'T'
    elif rsline.ccorr: 
      classchar = 'C'
    else:
      classchar = '3'

    classes[wid] = classchar
    corrections[wid] = corrected
    # print wid, classchar, corrected

  return classes, corrections



if __name__ == "__main__": 
  if len(sys.argv) == 3:
    path = sys.argv[1]
    ocrpath = sys.argv[2]
  else:
    print 'Usage:',sys.argv[0],'<SingleFile.labeled> <OCR.output.txt>'
    sys.exit(1)
  cls, cor = MyLabelExtract(path, ocrpath)
  print cls
  print cor
  print [x for x in cls if cls[x] == '0']

