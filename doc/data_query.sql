
select count(*) as supv_label from output_candidates as c right outer join orderaware_supv_label as s on c.id = s.candidate_id 
where s.label =true
;
-- super group by

select docid,
array_agg(id order by varid, candid, wordid) as arr_id,
array_agg(candidate_id order by varid, candid, wordid) as arr_candidate_id,
array_agg(varid order by varid, candid, wordid) as arr_varid,
array_agg(candid order by varid, candid, wordid) as arr_candid,
array_agg(wordid order by varid, candid, wordid) as arr_wordid,
array_agg(word order by varid, candid, wordid) as arr_word
from cand_word
group by docid

select max(candidate.docid) as docid, max(candidate.varid) as varid, max(candidate.candid) as candid, max(candidate.source) as source, max(candidate_id) as candidate_id, array_agg(word), label from candidate, cand_word where candidate.id = candidate_id group by candidate_id,label order by docid, varid, candid;

select candidate_id from cand_word as c, html_1gram as h where c.docid = h.docid and c.word = h.word1

SELECT dd_graph_weights.*, dd_inference_result_weights.weight FROM dd_graph_weights JOIN dd_inference_result_weights ON dd_graph_weights.id = dd_inference_result_weights.id ORDER BY abs(weight)

-- A General script for reasoning and examining the calibration plot
create view dd_inference_result_variables_mapped_factors as
select
  e.variable_id,
  e.factor_id,
  v.expectation,
  w.description, 
  resw.weight
from 
  dd_inference_result_variables as v,
  dd_inference_result_weights as resw,
  dd_graph_edges as e,
  dd_graph_factors as f,
  dd_graph_weights as w
where e.variable_id = v.id
  and e.factor_id = f.id
  and f.weight_id = w.id
  and resw.id = w.id
order by variable_id, factor_id
;


-- Check each variable's connected factors
create view reasoning as
select
  c.candidateid,
  e.factor_id,
  c.docid,
  c.wordid,
  c.candid,
  c.source,
  c.word,
  c.expectation,
  c.bucket,
  w.description, 
  w.weight
  from 
  output_candidates as c,
  dd_graph_edges as e,
  dd_graph_factors as f,
  dd_inference_result_variables_mapped_weights as w
where e.variable_id = c.id
  and e.factor_id = f.id
  and f.weight_id = w.id
order by c.id
;

select * from reasoning
into reasoning_0511
order by docid, wordid, candid;


-- Aggregate the table
create view reasoning as
select c.id, 
  max(candidateid) as candidateid, 
  max(docid) as docid, 
  max(wordid) as wordid, 
  max(candid) as wordid, 
  max(source) as source, 
  max(word) as word, 
  max(expectation) as expectation, 
  max(bucket) as bucket, 
  (select distinct _
    from array_agg(w.description || ' ' || ROUND( CAST (w.weight as numeric), 2)) as _) as connected_factors
from 
  output_candidates as c,
  dd_graph_edges as e,
  dd_graph_factors as f,
  dd_inference_result_variables_mapped_weights as w
where e.variable_id = c.id
  and e.factor_id = f.id
  and f.weight_id = w.id
group by c.id
order by c.id
;

-- Check fi problem
select * from candidate as c1,candidate as c2 where c1.docid = c2.docid and c1.wordid = c2.wordid and c1.word = 'first' and c2.word != c1.word limit 10;


 select c1.*, probability from (cand_with_label as c1 left join cand_label_label_inference as c2 on c1.id=c2.candidateid) where c1.docid='JOURNAL_145413';
 
SELECT * FROM 
(cand_label right join candidate on cand_label.candidateid = candidate.id)
        where word in 
        (select gram from ngram_1 where count > 1000);
---


select c1.id as "c1.id", c2.id as "c2.id", l1.id as "l1.id", l2.id as "l2.id", l1.label as "l1.label", l2.label as "l2.label"
from candidate as c1, candidate as c2, 
  cand_label as l1, cand_label as l2
where c1.id = l1.candidateid and c2.id = l2.candidateid
  and c1.docid = c2.docid 
  and c1.wordid = c2.wordid - 1
  and c1.word||' '||c2.word in 
  (select gram from ngram_2 where count > 100);