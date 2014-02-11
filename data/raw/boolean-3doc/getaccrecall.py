#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re
import pprint
import itertools
pp = pprint.PrettyPrinter(indent=2) # pretty printer

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

class ResultLine:
  def __init__(self):
    self.numwords = []
    self.tcorr = False
    self.ccorr = False
    self.rules = []  # arrays of Sets.

def CalcLesion(comb, lesionmap, reslines):
  lesionnum = 0
  for rsline in reslines:
    solvable = False
    for r in rsline.rules:  # All in r is needed
      if len(r.intersection(comb)) == 0:  # Remove none of the rules
        solvable = True
        break
    if not solvable:
      lesionnum += rsline.numwords

  lesionmap[comb] = lesionnum


def CalcNonTrivialLesion(comb, lesionmap, nontrivialmap, reslines):
  maxsublesion = 0  # Max lesion for sub-combinations
  if comb not in lesionmap:
    CalcLesion(comb, lesionmap)
  lesionnum = lesionmap[comb]
  if combsize > 0:
    for subset in itertools.combinations(comb, combsize - 1):
      if maxsublesion < lesionmap[subset]:
        maxsublesion = lesionmap[subset]
  if lesionnum > 0 and lesionnum > maxsublesion and len(comb) > 0:
    nontrivialmap[comb] = (lesionnum - maxsublesion, lesionnum)

def CalcForward(comb, forwardmap, reslines):
  recallnum = 0
  for rsline in reslines:
    solvable = False
    for r in rsline.rules:  # All in r is needed
      if r.issubset(comb):  # covered
        solvable = True
        break
    if solvable:
      recallnum += rsline.numwords

  forwardmap[comb] = recallnum

if __name__ == "__main__": 
  if len(sys.argv) == 2:
    path = sys.argv[1]
  else:
    print 'Usage:',sys.argv[0],'<SingleFile>'
    sys.exit(1)

  lines = [l.strip(' \n') for l in open(path).readlines()]

  tot_doc = 0       # For recall
  diff_doc = 0      # For recall on disagreed outputs
  tot_ocr = [0, 0]  # For acc
  non_correct = 0   # Both OCR fails
  correct = [0, 0]  # OCR results
  diff_correct = [0, 0]  # OCR results on disagreed words
  solved = 0        # If apply all rules, how many correct answers recalled



  tags = sorted([l.strip() for l in open('rule-tags.md').readlines()])
  
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

  for thisl in lines:
    l = thisl
    
    if l == '':  # empty line
      continue

    if '///' in l:
      l = l.replace('///', '|||')

    w1 = l[3:18].strip(' ')   # TODO: what if too long?
    w2 = l[19:19+15].strip(' ')

    l = l.split('|||')
    # print l

    if len(l) < 2:  # agreed
      tot_doc += 1
      for i in (0,1):
        tot_ocr[i] += 1
        correct[i] += 1
      for sol in know_tot: 
        know_tot[sol] += 1  # all solutions can solve it
      continue

    args = [p.strip(' ') for p in l[1].split('$')]
    # sol_str = [s.strip() for s in args[0].split(',')]
    sol_str = args[0]
    answers = args[1:]

    if len(answers) == 0:  # no mark, ignore this word.
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
    rsline.rules = sets # Sets
    rsline.tcorr = (answers[0] == '1')
    rsline.ccorr = (answers[0] == '2')
    rsline.numwords = this_num
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

  knowledge_classes = {
    'ocr': ('twchar', 'cwchar', 'upp', 'charuni', 'comb', 'url', 'dot', 'upper'),
    'corpus': ('d', 'sw', 'swgram', 'statc'),
    'corpus.single': ('d','sw','statc'),
    'corpus.ngram': ('swgram',),
    'nlp': ('pos','ner','number','persondot','lemma','path','by','etal'),
    'kb': ('kbe','kbr'),
    'ocr+corpus': ('d', 'sw', 'swgram', 'statc', 'twchar', 'cwchar', 'upp', 'charuni', 'comb', 'url', 'dot', 'upper'),
    'edit': ('ed', 'edrule', 'seg', 'rmchar', 'numconf'),
    'noedit': ('twchar', 'cwchar', 'upp', 'charuni', 'comb', 'url', 'dot', 'upper', 'ocrdocacc', 'statc', 'statcgram', 'sw', 'swgram', 'stats', 'd', 'pos', 'posgram', 'ner', 'number', 'persondot', 'by', 'etal', 'lemma', 'path', 'kbe', 'kbr'),
    'ocr+corpus+edit': ('d', 'sw', 'swgram', 'statc', 'twchar', 'cwchar', 'upp', 'charuni', 'comb', 'url', 'dot', 'upper','ed', 'edrule', 'seg', 'rmchar', 'numconf'),
    'all': ('twchar', 'cwchar', 'upp', 'charuni', 'comb', 'url', 'dot', 'upper', 'ocrdocacc', 'statc', 'statcgram', 'sw', 'swgram', 'stats', 'd', 'pos', 'posgram', 'ner', 'number', 'persondot', 'by', 'etal', 'lemma', 'path', 'kbe', 'kbr', 'ed', 'edrule', 'seg', 'rmchar', 'numconf')
  }

  # Sort the tuples
  knowledge_classes = {k:tuple(sorted(knowledge_classes[k])) for k in knowledge_classes}


  # lesionmap = {(t):0 for t in tags}  # Rule -> losetags
  lesionmap = {}  # Rule -> losetags. 
  # NOTE: lesionmap[()] is unsolvable cases. 

  nontrivialmap = {}
  for combsize in range(0, 4):  # 0 for no-rule lesion...
    for comb in itertools.combinations(tags, combsize):
      CalcLesion(comb, lesionmap, reslines)
      CalcNonTrivialLesion(comb, lesionmap, nontrivialmap, reslines)

  numunsolvable = lesionmap[()]
  print 'Unsolvable:', numunsolvable
  if diff_doc - solved != numunsolvable:
    print 'Error calculating unsolvable!'
    sys.exit(1)


  forwardmap = {}  # Rule -> losetags. 
  for key in knowledge_classes:
    comb = knowledge_classes[key]
    CalcLesion(comb, lesionmap, reslines)
    print key
    print '  LES ',lesionmap[comb]-numunsolvable

    CalcForward(comb, forwardmap, reslines)
    print '  FWD ',forwardmap[comb]

  
  

  # Interesting combinations have high "delta".
  # pp.pprint([(nontrivialmap[t], t) for t in sorted(nontrivialmap, key=nontrivialmap.get) if nontrivialmap[t][0] >= 5 or len(t) == 1])

  fout = open('stats/'+path+'.stat.txt', 'w')
  print 'Diff',diff_doc, 'Tot',tot_doc, 'TOTOCR',tot_ocr, 'CORRECT',correct, 'NONCORRECT',non_correct


  print >>fout, 'Total document words:',tot_doc
  print >>fout, ''

  print >>fout, 'Total OCR output words:'
  TCPrinter(tot_ocr, fout)
  print >>fout, ''

  print >>fout, 'OCR correct outputs:'
  TCPrinter(correct, fout)
  print >>fout, ''

  print >>fout, 'Words where all OCRs fail:',non_correct, '(%.4f%%)' % (non_correct*100.0 / tot_doc)
  print >>fout, ''

  print >>fout, 'Accuracy:'
  TCPrinter(['%.4f%%' % (100.0 * correct[i] / float(tot_ocr[i])) for i in (0,1)], fout)
  print >>fout, ''

  print >>fout, 'Recall on total document:'
  TCPrinter(['%.4f%%' % (100.0 * correct[i] / float(tot_doc)) for i in (0,1)], fout)
  print >>fout, ''

  print >>fout, 'Words where at least 1 OCR make errors (disagreed / agreed but both failed):',diff_doc, '(%.4f%%)' % (100.0 * diff_doc / float(tot_doc))

  print >>fout, 'Automatically solvable errors:', solved, '(%.4f%%)' % (100.0 * solved / float(diff_doc))
  print >>fout, ''

  print >>fout, 'Recall on error (disagree / both fail) words:'
  TCPrinter(['%.4f%%' % (100.0 * diff_correct[i] / float(diff_doc)) for i in (0,1)], fout)
  print >>fout, ''


  
  

  # print >>fout, '\nRecall for each knowledge on all words:'
  # for s in ['%10s: %.4f%%' % (t, know_tot[t] / float(tot_doc) * 100.0 )
  #     for t in sorted(know_tot, key=know_tot.get, reverse=True)]:
  #   print >>fout,'  '+s

  print >>fout, '\nRecall for each knowledge on error words:'
  for s in ['%10s: %.4f%%' % (t, know_disagree[t] / float(diff_doc) * 100.0 )
      for t in sorted(know_disagree, key=know_disagree.get, reverse=True)]:
    print >>fout,'  '+s

  print >>fout, '\nRecall for each knowledge on words where OCRs all fail:'
  for s in ['%10s: %.4f%%' % (t, know_noncorrect[t] / float(non_correct) * 100.0 )
      for t in sorted(know_noncorrect, key=know_noncorrect.get, reverse=True)]:
    print >>fout,'  '+s

  print >>fout, '\nLesion for each knowledge on error words:'
  for s in [t for t in sorted(nontrivialmap, key=nontrivialmap.get, reverse=True) if nontrivialmap[t][0] >= 5 or len(t) == 1]:
    if len(s) > 1:
      print >>fout, '%20s: %.4f%% (%.4f%% more)' % (','.join(s), (nontrivialmap[s][1] - numunsolvable) * 100.0 / float(diff_doc), nontrivialmap[s][0] * 100.0 / float(diff_doc))
    else:
      print >>fout, '%20s: %.4f%%' % (','.join(s), (nontrivialmap[s][1] - numunsolvable) * 100.0 / float(diff_doc))

  print >>fout, '\nLesion (backward search) for each knowledge class, recall on error words:'
  for key in knowledge_classes:
    comb = knowledge_classes[key]
    # print lesionmap[comb], key, comb
    print >>fout, '%15s: %.4f%%' % (key, (lesionmap[comb] - numunsolvable) * 100.0 / float(diff_doc))

  print >>fout, '\nFoward search for each knowledge class, recall on error words:'
  for key in knowledge_classes:
    comb = knowledge_classes[key]
    # print lesionmap[comb], key, comb
    print >>fout, '%15s: %.4f%%' % (key, forwardmap[comb] * 100.0 / float(diff_doc))


  fout.close()

