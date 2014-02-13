create table features(id BIGSERIAL PRIMARY KEY, 
  docid TEXT, 
  wordid INT, 
  feature_name TEXT, 
  feature_val BOOLEAN);

create table labels(id bigserial primary key, 
  docid TEXT, 
  wordid INT, 
  label_t BOOLEAN, 
  label_c BOOLEAN);

create table actual_words(id bigserial primary key, 
  docid TEXT, 
  wordid INT, 
  word TEXT);

create table options(id bigserial primary key, 
  docid TEXT, 
  wordid INT, 
  option_t TEXT, 
  option_c TEXT);



# QUERY!!!
-- select lt.docid, lt.wordid, lt.label_t, lt.label_c, lt.probability as p_t, lc.probability as p_c

create view compare_results as
select lt.docid, lt.wordid, lt.probability as p_t, lc.probability as p_c
from filtered_labels_label_t_inference as lt INNER JOIN filtered_labels_label_c_inference as lc ON lt.docid =lc.docid and lt.wordid=lc.wordid;

select count(*) from compare_results INNER JOIN labels 
ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid 
-- WHERE label_t != label_c;

# TOTAL

select count(*) from compare_results INNER JOIN labels 
ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid 
WHERE (label_t = True and p_t > p_c) 
  OR (label_c = True and p_t < p_c);

# Precision / Recall


-- 14GB text, ~15k documents:
-- /lfs/madmax3/0/czhang/cleanpaleo/NLPRS_jan20_overlap.22

-- Add a line row_number:
-- select row_number() over(order by docid, wordid) as rownum, t.* from filtered_labels as t;

\set foldnum 10
\set thisfold 1
\set numrows 'select count(*) from filtered_labels'

UPDATE filtered_labels
  SET label_t = NULL, label_c = NULL
  where id < (:numrows) * :thisfold / :foldnum and id >= (:numrows) * (:thisfold - 1) / :foldnum;


-- select count(*) from filtered_labels where id < (:numrows) * :thisfold / :foldnum and id >= (:numrows) * (:thisfold - 1) / :foldnum;




---------------

drop view if exists compare_results;
create view compare_results as
select lt.docid, lt.wordid, lt.probability as p_t, lc.probability as p_c
from filtered_labels_label_t_inference as lt INNER JOIN filtered_labels_label_c_inference as lc ON lt.docid =lc.docid and lt.wordid=lc.wordid;

COPY (
select count(*) from compare_results INNER JOIN labels 
  ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid) 
TO '/tmp/ddocr_diff.tsv';

COPY(
select count(*) from compare_results INNER JOIN labels 
ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid 
WHERE (label_t = True and p_t > p_c) 
  OR (label_c = True and p_t < p_c)
) TO '/tmp/ddocr_correct.tsv';

COPY(
select count(*) from compare_results INNER JOIN labels 
ON compare_results.docid = labels.docid and compare_results.wordid = labels.wordid WHERE (label_t = True OR label_c = True)
) TO '/tmp/ddocr_fixable.tsv'