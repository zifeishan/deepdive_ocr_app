-- NO NATURAL JOINS!!!!
create table cand_label(id BIGSERIAL PRIMARY KEY, 
  candid BIGSERIAL REFERENCES candidate(id),
  label BOOLEAN);

-- select distinct docid into document from candidate;
drop table if exists document;
create table document(id bigserial primary key, docid text);
insert into document(docid) select distinct docid from candidate;


create table html_1gram(id BIGSERIAL PRIMARY KEY, 
  docid TEXT,
  word1 TEXT,
  freq INT);

create table html_2gram(id BIGSERIAL PRIMARY KEY, 
  docid TEXT,
  word1 TEXT,
  word2 TEXT,
  freq INT);

create table html_3gram(id BIGSERIAL PRIMARY KEY, 
  docid TEXT,
  word1 TEXT,
  word2 TEXT,
  word3 TEXT,
  freq INT);

create table candidate(id BIGSERIAL PRIMARY KEY, 
  docid TEXT,
  wordid INT,
  candid INT,
  source TEXT,
  word TEXT);

-- JOURNAL_28971 1 0 C Cretaceous

create table cand_box(id BIGSERIAL PRIMARY KEY, 
  docid TEXT, 
  wordid INT, 
  candid INT,
  page INT,
  l INT,
  t INT,
  r INT,
  b INT);

-- JOURNAL_28971 1 0 1 1003  202 1132  221

create table cand_feature(id BIGSERIAL PRIMARY KEY, 
  docid TEXT, 
  wordid INT, 
  candid INT,
  pos TEXT,
  ner TEXT,
  stem TEXT);

-- JOURNAL_28971 1 1 JJ  ORGANIZATION  cretaceous

create table feature(id BIGSERIAL PRIMARY KEY, 
  candidateid BIGSERIAL REFERENCES candidate(id),
  fname TEXT,
  fval BOOLEAN);








-----------

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



--------------

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