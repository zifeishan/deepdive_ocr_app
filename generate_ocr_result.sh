psql -c """drop table if exists output_candidates cascade; """ ddocr

psql -c """select candidate.*, probability, bucket, random() as random_number
into output_candidates
from cand_label_label_inference_bucketed right join candidate on candidateid=candidate.id 
 where docid in (select * from eval_docs) 
 order by docid, wordid, random_number
;
""" ddocr

psql -c """create view maxp as 
select docid, wordid, max(probability) as maxp, max(random_number) as maxrand 
from output_candidates group by docid,wordid;
""" ddocr

psql -c """create view output_words as
  select * from output_candidates join maxp
  on  output_candidates.docid = maxp.docid
  and output_candidates.wordid = maxp.wordid
  and output_candidates.probability = maxp.maxp
  and output_candidates.random_number = maxp.maxrand
;""" ddocr

psql -c """create view output_words as
  select * from output_candidates join maxp
  on  output_candidates.docid = maxp.docid
  and output_candidates.wordid = maxp.wordid
  and output_candidates.probability = maxp.maxp
  and output_candidates.random_number = maxp.maxrand
;""" ddocr

psql -c """copy (select docid, wordid, word from output_words order by docid, wordid) 
to '/tmp/ocr-output-words.tsv';""" ddocr
