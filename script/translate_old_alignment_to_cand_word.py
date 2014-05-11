import sys, os

data_dir = 'journals-output/'
outputbase = ''
if len(sys.argv) == 3:
  data_dir = sys.argv[1] + '/'
  outputbase = sys.argv[2] + '/'
else:
  print 'Usage:',sys.argv[0],'<data_dir, e.g. journals-output> <outputbase>'
  sys.exit(1)


article_count = 0
ids = [i[:-len('.cand')] for i in os.listdir(data_dir) if i.endswith('.cand')]
for fid in ids:
  print 'Processing', fid, 'total:',article_count
  article_count += 1
  cand = open(data_dir + fid + '.cand').readlines()
  candfeat = open(data_dir + fid + '.candfeature').readlines()
  candbox = open(data_dir + fid + '.candbox').readlines()

  fcandword = open(outputbase + fid + '.cand_word', 'w')

  feat_id = 0

  lastdocid = ''
  lastvarid = ''
  source_candid = {}
  source_wordid_counter = {} # count how many words are in different candidates

  for i in range(len(cand)):
    parts_cand = cand[i].strip().split('\t')
    parts_box = candbox[i].strip().split('\t')
    ocrid = parts_cand[3]
    if ocrid == 'T':
      features = candfeat[feat_id]
      feat_id += 1
      parts_feat = features.strip().split('\t')
    else:
      parts_feat = [''] * 6 

    docid = parts_cand[0]
    varid = parts_cand[1]
    # candid_tot = parts_cand[2]
    source = parts_cand[3]
    word = parts_cand[4]
    box = parts_box[3:]
    feature = parts_feat[3:]

    if lastdocid != docid or lastvarid != varid:  # clean counter
      source_candid = {}
      source_wordid_counter = {}

    lastdocid = docid
    lastvarid = varid

    if source not in source_candid:
      source_candid[source] = len(source_candid)  # start from 0
      source_wordid_counter[source] = 0
      # print docid, varid, source_candid, source_wordid_counter
      # raw_input()

    candid = str(source_candid[source])
    wordid = str(source_wordid_counter[source])
    source_wordid_counter[source] += 1

    print >>fcandword, '\t'.join([docid, varid, candid, source, wordid, word] + box + feature)
  if feat_id != len(candfeat):
    print 'ERROR: feat_id not correct'

  fcandword.close()








  
