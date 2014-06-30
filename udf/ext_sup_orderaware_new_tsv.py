#! /usr/bin/python

import sys, os, codecs

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(BASE_DIR + '/../util')
# import latticematch
import latticematch_singlepath as latticematch

# Import query:
'''
SELECT  docid,
        array_to_string(array_agg(candidate_id order by varid, candid, wordid), ',' ) AS arr_candidate_id,
        array_to_string(array_agg(varid order by varid, candid, wordid), ',' ) AS arr_varid,
        array_to_string(array_agg(wordid order by varid, candid, wordid), ',' ) AS arr_wordid,
        array_to_string(array_agg(word order by varid, candid, wordid), '~~~^^^~~~' ) AS arr_word
FROM    cand_word
GROUP BY docid
'''

SUPV_DIR = os.environ['SUPV_DIR']
# SUPV_DIR='/dfs/hulk/0/zifei/ocr/supervision_escaped/'
bestpick_dir = ''

OUTPUT_FREQUENCY = 1

# Accept arguments for using specific SUPV_DIR.
if len(sys.argv) >= 3:
  bestpick_dir = sys.argv[1]
  SUPV_DIR = sys.argv[2]
  print >>sys.stderr, "NOTE: you should already EMPTY the directory", SUPV_DIR
  print >>sys.stderr, "Using EVAL_DIR as SUPV_DIR:", SUPV_DIR
  print >>sys.stderr, "Storing bestpick results into:", bestpick_dir

tot_edge_count = 0

# Build graph
def AddEdge(edges, f, t):
  if f not in edges:
    edges[f] = []
  edges[f].append(t)
  global tot_edge_count
  tot_edge_count += 1


################## MAIN FUNCTION ####################

rowcount = 0

for row in sys.stdin:
# for row in open('/tmp/ext_sup_orderaware_tsv.input').readlines():

  docid, varids, candids, wordids, words = row.rstrip('\n').split('\t')
  varids = [int(x) for x in varids.split(',')]
  candids = [int(x) for x in candids.split(',')]
  wordids = [int(x) for x in wordids.split(',')]
  words = words.split('~~~^^^~~~')

  # DEBUG
  SAMPLESIZE = 1000
  varids = varids[:SAMPLESIZE]
  candids = candids[:SAMPLESIZE]
  wordids = wordids[:SAMPLESIZE]
  words = words[:SAMPLESIZE]

  # They should have same length
  assert len(words) == len(varids) and len(words) == len(candids) and len(words) == len(wordids)
  rowcount += 1
  N = len(varids)  # number of words
  if N == 0:
    print >>sys.stderr, 'Empty data:',str(docid)
    continue

  # build candidate_id array
  unique_wordids = [str(varids[i]) + '_' + str(candids[i]) + '.' + str(wordids[i]) for i in range(N)]
  # docid + [this] == candidate_id

  # Load transcript (supervision sequence)
  transcript_file = SUPV_DIR + '/' + docid + '.seq'
  if not os.path.exists(transcript_file):
    print >>sys.stderr, 'SUPERVISION DATA NOT EXISTS:', transcript_file
    continue

  # array of words
  # TODO l.strip().decode('utf-8')
  transcript = [l.strip() for l in open(transcript_file).readlines()]

  # DEBUG
  transcript = transcript[:SAMPLESIZE]
  # for i in range(20):
  #   print varids[i], candids[i], wordids[i], words[i]
  # print transcript

  # Build index for candidate_id
  index_cid_sub = {}
  for sub in range(N):
    cid = unique_wordids[sub]
    index_cid_sub[cid] = sub

  # Build index
  index_vcw_sub = {}
  index_vc_maxwid = {}

  # print 'N:',N
  for sub in range(N):
    v = varids[sub]
    c = candids[sub]
    w = wordids[sub]
    if v not in index_vcw_sub:
      index_vcw_sub[v] = {}
      index_vc_maxwid[v] = {}
    if c not in index_vcw_sub[v]:
      index_vcw_sub[v][c] = {}
      index_vc_maxwid[v][c] = 0  # assume v,c,0 must exist
    
    index_vcw_sub[v][c][w] = sub
    if w > index_vc_maxwid[v][c]:
      index_vc_maxwid[v][c] = w

  ######### 1. build directed graph

  # Note that input is sorted by (varid, candid, wordid)
  # Init edges
  edges = {}  # cand_word_id1 : [cand_word_id2]
  for cid in index_cid_sub: edges[cid] = []
  
  # compute all edges
  for i in range(N):
    v = varids[i]
    c = candids[i]
    w = wordids[i]
    # print v, c, w
    # print index_vc_maxwid
    lastwid = index_vc_maxwid[v][c]
    # not the last word. sorted by (varid, candid, wordid)!

    if w != lastwid: # not the last word in candidate
      j = i + 1
      # print j, N
      if j < N: 
        AddEdge(edges, unique_wordids[i], unique_wordids[j])
    else:  # last word in candidate. 
      # Add an edge to all candidates in NEXT VARID.
      # TODO: consider skipping triangle case!!
      if v + 1 in index_vcw_sub:
        for c in index_vcw_sub[v + 1]:
          j = index_vcw_sub[v + 1][c][0]
          AddEdge(edges, unique_wordids[i], unique_wordids[j])

  print >>sys.stderr, "#Edges: ", tot_edge_count
  # DEBUG
  # print '\n'.join([k +'\t'+ str(edges[k]) for k in sorted(edges.keys())])
  ############# 2. Return DP result

  # def run(docid, starts, ends, candidates, unique_wordids, transcript):
  score, match_pairs, path_mat, f = latticematch.Match(words, transcript, \
    edges, unique_wordids, index_cid_sub)

  # DEBUG
  # print '================'
  # plpy.info('BEST SCORE: %d' % score)
  # print 'Match pairs:', match_pairs  # (latticeIndex, transcriptIndex)
  latticematch.PrintStatus(f,path_mat)

  # Deduplication
  match_subs = set([p[0] for p in match_pairs])

  # a set of CIDs from the match
  match_cids = set([unique_wordids[i] for i in match_subs])

  true_cids = match_cids

  match_candidate_ids = set( [docid + '@' + cid.split('.')[0] for cid in true_cids])

  # TODO should we consider only candidates that ALL words matches??
  # now we consider candidiates that at least one word match...
  for cid in sorted(match_candidate_ids):
    # yield docid, cid, True
    print '\t'.join([str(_) for _ in [docid, cid, 'true']])

  # false_cids = set(unique_wordids).difference(true_cids)
  # for cid in false_cids:
  #   # yield docid, cid, False
  #   print '\t'.join([str(_) for _ in [docid, cid, 'false']])

  if (rowcount - 1) % OUTPUT_FREQUENCY == 0:  # Sample screenlog output
    print >>sys.stderr, '[%s]  SCORE: %d / %d (%f), matches: %d / %d' % (docid, score, len(transcript), float(score)/len(transcript), len(true_cids), len(unique_wordids))


