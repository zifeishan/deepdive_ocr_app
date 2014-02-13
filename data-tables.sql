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
create view compare_results as
select lt.docid, lt.wordid, lt.probability as p_t, lc.probability as p_c
from filtered_labels_label_t_inference as lt INNER JOIN filtered_labels_label_c_inference as lc ON lt.docid =lc.docid and lt.wordid=lc.wordid;

select count(*) from compare_results, labels where labels.label_t != label_c;
# 52
select count(*) from compare_results 
WHERE label_t != label_c AND 
  (label_t = True and p_t > p_c) 
  OR (label_c = True and p_t < p_c);
# 44


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

