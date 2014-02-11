#!/usr/bin/python

import os, sys
from util import *
# from nltk.corpus import wordnet as wn
# import enchant
import featureextractor
import naivefeature
import mylabelextractor
import re

numSuggestions = 0

def FeatureExtract(alignedfile, labels, corrections, corpus ={}, startingid = 0, featureset = set(), featurenameset = set(), docid = '', outputbase = ''):
  words = [line.strip().split('\t') for line in open(alignedfile).readlines()]

  options = []
  
  feature_names = []

  if outputbase == '':
    filebase = alignedfile[:-len('.output.txt')] # remove ".outpu..."
    filebase += '.'
  else:
    filebase = outputbase + '/' + docid + '.'
  print 'savebase:', filebase
  fopt = open(filebase + 'options.txt', 'w')
  fftr = open(filebase + 'features.txt', 'w')
  flab = open(filebase + 'labels.txt', 'w')
  fcor = open(filebase + 'corrected_words.txt', 'w')

  naivefeature.occurweb.ReadDict()

  # 1 JIM JIM NNP PERSON  JIM nn  3 273 ['P11,1732 2036 1855 2083']
  wid = -1  # Start from 0
  for word in words: 
    if len(word) <= 1: continue  # Empty line
    # FIXED!!

    wid += 1
    if startingid > wid: continue

    # word[1]: Tesseract
    # word[2]: Cuneiform

    # options = [word[2], word[1]]  # TODO!!!! 
    options = [word[1], word[2]]  # NEW!!!


    # stripped = [Strip(w) for w in options]
    # stripped = [w for w in options]  # DO NOT STRIP WORDS NOW!!

    if word[1] == '' and word[2] == '':  # no \w
      # print 'Skip:', options
      continue

    # No labels & same: both true
    if wid not in labels and word[1] == word[2]:
      labels[wid] = '0'

    if wid not in labels: 
      print 'Missing labels for word', wid, word[1], word[2]
      # raw_input()
      continue

    
    this_features = []
    this_feature_names = []

    # Do not get suggestions: numSuggestions = 0
    sugg_tuples = GetSuggestionsFromCorpus(options, corpus, numSuggestions)

    suggs = [s[1] for s in sugg_tuples]
    suggs = suggs[:numSuggestions]
    if len(suggs) < numSuggestions:
      suggs += ['']*(numSuggestions - len(suggs))

    # print wid, options

    fnames, ftrs = featureextractor.FeatureExtractAllOptions(options, isBoolean=True)
    this_features = ftrs
    this_feature_names = fnames # not efficient

    # Handle suggestions
    fnames, ftrs = featureextractor.FeatureExtractAllSuggestions(options, suggs, corpus)

    this_features += ftrs
    this_feature_names += fnames # not efficient

    # for i in range(0, len(this_features)):
    #   # Filter features to output
    #   if i not in featureset or len(featureset) == 0:
    #     continue


    # Print to "TSV" files: docid \t wid \t ...
    didwid = [str(docid), str(wid)]
    print >>fopt, '\t'.join(didwid + options)

    # if len(featureset) > 0:
    #   print >>fftr, '\t'.join(didwid + 
    #     [str(this_features[i]) for i in range(0, len(this_features)) if i in featureset])
    # elif len(featurenameset) > 0:
    #   print >>fftr, '\t'.join(didwid +
    #     [str(this_features[i]) for i in range(0, len(this_features)) if this_feature_names[i] in featurenameset])
    # else:
    #   print >>fftr, '\t'.join(didwid + 
    #     [str(i) for i in this_features])

    # Print a thin table for evry docid, wid, fname, fval
    for i in range(0, len(this_features)):
      print >>fftr, '\t'.join(didwid + 
        [this_feature_names[i], str(this_features[i])]
        )  

    # print >>fftr, '\t'.join([str(i) for i in this_features])
    fopt.flush()
    fftr.flush()


    label = labels[wid]
    
    # Output: Binary_labels, corrected word
    bool_labels = [False] * (len(options) + len(suggs))
    corrected = ''
    
    if label == '0':  # Both right
      corrected = options[0]  # first option is correct.. ? TODO
      for i in range(0, len(options)):
        bool_labels[i] = True

    elif label == 'T':  # TODO Haowen's 1 means 
      corrected = options[0]
      bool_labels[0] = True

    elif label == 'C':  # TODO Haowen's 1 means 
      corrected = options[1]
      bool_labels[1] = True

    elif label == '3':  # none-right
      # label = len(suggs) + len(options) + 1 # None-right label
      corrected = '???'
      # bool_labels all false
    else:
      print 'Warn: label', label

    if wid in corrections:
      corr = corrections[wid]
      corrected = corr

      # TODO handle suggestions...
      for i in range(0, len(suggs)):
        if suggs[i] == corr.strip(',.?!}{[]-_'):  # TODO strip..
        # if suggs[i] == Strip(corr):
          # label = len(options) + i + 1
          bool_labels[len(options) + i] = True
          corrected = corrections[wid]

          print 'Correct:', corrections[wid], 'label:', len(options) + i + 1

    # print corrected, options
    # print bool_labels
    # if label != '0':
    #   raw_input()

    print >>flab, '\t'.join(didwid + [str(b) for b in bool_labels])

    print >>fcor, '\t'.join(didwid + [corrected])

    flab.flush()
    fcor.flush()

    feature_names =  this_feature_names

  fopt.close()
  fftr.close()
  flab.close()
  fcor.close()


  fout = open(filebase+'feature_names.txt', 'w')
  if len(featureset) > 0:
    for i in range(0, len(feature_names)):
      if i in featureset:
        print >>fout, feature_names[i]
  elif len(featurenameset) > 0:
    for i in range(0, len(feature_names)):
      if i in featurenameset:
        print >>fout, feature_names[i]
  else:
    for i in range(0, len(feature_names)):
      print >>fout, feature_names[i]        
  fout.close()

  naivefeature.occurweb.WriteDict()

def HaowenLabelExtract(haowen_labeled_file):
  classes = {}  # WID, label
  corrections = {}
  
  casenum = 0

  lines = open(haowen_labeled_file).readlines()
  
  wid = -1
  for l in lines:
    wid += 1
    l = l.rstrip('\n')

    if not l.startswith('X'):
      continue

    l = l[1:]
    classchar = l[0]
    if classchar not in  ['1', '2', '3']:
      print classchar
      continue

    casenum += 1

    # REVERSE CHAR for Tess/Cuni!!!
    if classchar == '1': 
      classchar = 'T'
    elif classchar == '2': 
      classchar = 'C'

    classes[wid] = classchar

    l = l[2:]
    if l.startswith(' '):  # No corrections
      continue

    l = re.sub(' +',' ',l)
    parts = l.split(' ')
    # print len(parts), parts
    corr = parts[0]
    corrections[wid] = corr


  print 'X Cases:',casenum
  filebase = haowen_labeled_file[:-len('.labeled.txt')] + '.'

  return classes, corrections



if __name__ == "__main__": 

  LABEL_TYPE_NEW = False

  if len(sys.argv) >= 3:
    dirbase = sys.argv[1]
    outputbase = sys.argv[2]
    if len(sys.argv) == 4:
      if sys.argv[3] == '1':
        LABEL_TYPE_NEW = True

  else:
    print 'Usage:',sys.argv[0],'<OCRoutput-dir-base/> <outputBase/> <IfExtractNewLabels = 0>'
    sys.exit(1)

  dirbase += '/'

  ids = [f[:-len('.output.txt')] for f in os.listdir(dirbase) if f.endswith('.output.txt')]

  # if len(idfilters) > 0:
  #   print 'Filter file', idfilters
  #   ids = set(ids).intersection(idfilters)

  print 'Process files:', ids


  # corpuspath = '../data/corpus-wordcount.txt'
  # corpus = {
  #   l.strip().split('\t')[0]:
  #   l.strip().split('\t')[1] 
  #   for l in open(corpuspath).readlines()
  # }

  for fid in ids:
    alignedfile = dirbase + fid + '.output.txt'
    

    # TODO EXTRACT LABELS SEPARATEDLY!!!!
    # TODO
    
    if not LABEL_TYPE_NEW:
      labeledfile = dirbase + fid + '.labeled.txt'
      cls, cor = HaowenLabelExtract(labeledfile)
    else:
      labeledfile = dirbase + fid + '.labeled'
      cls, cor = mylabelextractor.MyLabelExtract(labeledfile, alignedfile)

    FeatureExtract(alignedfile, cls, cor, 
      # corpus, 
      docid = fid,
      outputbase = outputbase
      # featurenameset=selfeaturenames
      # featureset = featureset
      )

  # print cor