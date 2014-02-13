#! /usr/bin/env python

# Call: /udf/kfold.py "${KFOLD_NUM}" "${KFOLD_ITER}"filtered_labels label_t label_c

import os, sys

p_diff = '/tmp/ddocr_diff.tsv'
p_corr = '/tmp/ddocr_correct.tsv'
p_fixable = '/tmp/ddocr_fixable.tsv'

q_stats = '''psql -c """
  drop view if exists compare_results;
  create view compare_results as
  select lt.docid, lt.wordid, lt.probability as p_t, lc.probability as p_c
  from filtered_labels_label_t_inference as lt INNER JOIN filtered_labels_label_c_inference as lc ON lt.docid =lc.docid and lt.wordid=lc.wordid;

  COPY (
  select count(*) from compare_results INNER JOIN labels 
    ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid) 
  TO \'''' + p_diff + '''\';

  COPY(
  select count(*) from compare_results INNER JOIN labels 
  ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid 
  WHERE (label_t = True and p_t > p_c) 
    OR (label_c = True and p_t < p_c)
  ) TO \'''' + p_corr + '''\';

  COPY(
  select count(*) from compare_results INNER JOIN labels 
  ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid WHERE (label_t = True OR label_c = True)
  ) TO \'''' + p_fixable + '''\';

  """ ddocr'''

os.system(q_stats)
diff = int(open(p_diff).readline().strip())
corr = int(open(p_corr).readline().strip())
fix = int(open(p_fixable).readline().strip())

fout = open('/tmp/evaluation.tsv', 'a')
print >>fout, '%d\t%d\t%d\t%.2f%%\t%.2f%%' % (diff, fix, corr, 100.0*corr/diff, 100.0*corr/fix)
