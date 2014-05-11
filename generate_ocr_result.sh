if [ $# = 1 ]; then
  export DBNAME=$1
else
  export DBNAME=ddocr
fi
echo "Set DB_NAME to ${DBNAME}."


export EXPORT_ROOT='/tmp'

psql -c """drop table if exists output_candidates, output_words cascade; """ $DBNAME

# psql -c """select cand_label_label_inference_bucketed.id as id, candidate.id as candidateid, docid, wordid, candid, source, word, expectation, bucket, random() as random_number
# into output_candidates
# from cand_label_label_inference_bucketed right join candidate on candidateid=candidate.id 
#  where docid in (select * from eval_docs) 
#  order by docid, wordid, random_number
# ;
# """ $DBNAME

psql -c """
CREATE TABLE output_candidates AS
select c.*, array_agg(word order by wordid) as word, random() as random_number
from candidate_label_inference_bucketed as c, cand_word
 where c.docid in (select * from eval_docs) 
 and cand_word.candidate_id = c.candidate_id
 group by 
 c.id, c.docid, c.candidate_id, c.variable_id, c.varid, c.candid, c.source, c.label, c.category, c.expectation, c.bucket, cand_word.candidate_id
 order by c.docid, c.varid, random_number
DISTRIBUTED BY (docid);
""" $DBNAME


psql -c """create view maxp as 
select variable_id, max(docid) as docid, max(varid) as varid, max(expectation) as maxp, max(random_number) as maxrand 
from output_candidates group by variable_id;
""" $DBNAME

psql -c """
  CREATE TABLE output_words AS 
    select output_candidates.*
    from output_candidates join maxp
    on  output_candidates.variable_id = maxp.variable_id
    and output_candidates.expectation = maxp.maxp
    -- and output_candidates.random_number = maxp.maxrand
  DISTRIBUTED BY (docid);
""" $DBNAME

# break ties
psql -c """delete from output_words
where id in 
(select w1.candidate_id
  from output_words as w1,
  output_words as w2 
  where w1.random_number < w2.random_number 
  and w1.variable_id = w2.variable_id)
;
""" $DBNAME

# psql -c """copy (select docid, varid || '-' || source || '-' || wordid, word from cand_word where candidate_id in (select id from output_words) order by docid, varid, candid, wordid) 
# to '$EXPORT_ROOT/ocr-output-words.tsv'""" $DBNAME

psql -c """COPY (SELECT * FROM eval_docs) 
to STDOUT """ $DBNAME > $EXPORT_ROOT/ocr-eval-docs.tsv


### TODO use same varid to enable strict evaluation matching
psql -c """copy (select docid, candidate_id, word from cand_word where candidate_id in (select candidate_id from output_words) order by docid, varid, candid, wordid) 
to '$EXPORT_ROOT/ocr-output-words.tsv'""" $DBNAME


psql -c """copy (select docid, candidate_id, word from cand_word 
  where (source = 'T' or source = 'CT' or source = 'TC')
  and docid in (select * from eval_docs)
  order by docid, varid, candid, wordid) to '$EXPORT_ROOT/ocr-output-words-tesseract.tsv'""" $DBNAME

psql -c """copy (select docid, candidate_id, word from cand_word 
  where (source = 'C' or source = 'CT' or source = 'TC')
  and docid in (select * from eval_docs)
  order by docid, varid, candid, wordid) to '$EXPORT_ROOT/ocr-output-words-cuneiform.tsv';""" $DBNAME

psql -c """drop view if exists reasoning;""" $DBNAME

psql -c """create view reasoning as
select
  c.id,
  c.candidate_id,
  e.factor_id,
  c.docid,
  c.varid,
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
order by c.docid, c.varid, c.candid
;""" $DBNAME
