export EXPORT_ROOT='/tmp'

psql -c """drop table if exists output_candidates cascade; """ ddocr

psql -c """select cand_label_label_inference_bucketed.id as id, candidate.id as candidateid, docid, wordid, candid, source, word, expectation, bucket, random() as random_number
into output_candidates
from cand_label_label_inference_bucketed right join candidate on candidateid=candidate.id 
 where docid in (select * from eval_docs) 
 order by docid, wordid, random_number
;
""" ddocr

psql -c """create view maxp as 
select docid, wordid, max(expectation) as maxp, max(random_number) as maxrand 
from output_candidates group by docid, wordid;
""" ddocr

psql -c """create view output_words as
  select output_candidates.* from output_candidates join maxp
  on  output_candidates.docid = maxp.docid
  and output_candidates.wordid = maxp.wordid
  and output_candidates.expectation = maxp.maxp
  and output_candidates.random_number = maxp.maxrand
;""" ddocr

psql -c """copy (select docid, wordid, word from output_words order by docid, wordid) 
to '$EXPORT_ROOT/ocr-output-words.tsv'""" ddocr

psql -c """copy (select docid, wordid, word from candidate 
  where source = 'T' and docid in (select * from eval_docs)
  order by docid, wordid, candid) to '$EXPORT_ROOT/ocr-output-words-tesseract.tsv'""" ddocr

psql -c """copy (select docid, wordid, word from candidate 
  where source = 'C' and docid in (select * from eval_docs)
  order by docid, wordid, candid) to '$EXPORT_ROOT/ocr-output-words-cuneiform.tsv';""" ddocr

psql -c """drop view if exists reasoning;""" ddocr

psql -c """create view reasoning as
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
;""" ddocr
