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