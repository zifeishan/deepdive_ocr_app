## Misalignment

ddocr_100_textid=# select * from output_words where word[1] like 'terminable' order by docid,varid,candid limit 20;
    variable_id    |     docid     | varid | candid | source | label |    candidate_id     |   id   | category | expectation | bucket |     word     |   random_number
-------------------+---------------+-------+--------+--------+-------+---------------------+--------+----------+-------------+--------+--------------+-------------------
 JOURNAL_13504@610 | JOURNAL_13504 |   610 |      0 | C      | f     | JOURNAL_13504@610_0 | 710990 |        1 |       0.008 |      0 | {terminable} | 0.459841592703015
(1 row)

ddocr_100_textid=# select * from output_candidates where variable_id='JOURNAL_13504@610' order by docid,varid,candid limit 20;
    variable_id    |     docid     | varid | candid | source | label |    candidate_id     |   id   | category | expectation | bucket |     word     |   random_number
-------------------+---------------+-------+--------+--------+-------+---------------------+--------+----------+-------------+--------+--------------+-------------------
 JOURNAL_13504@610 | JOURNAL_13504 |   610 |      0 | C      | f     | JOURNAL_13504@610_0 | 710990 |        1 |       0.008 |      0 | {terminable} | 0.459841592703015
(1 row)

ddocr_100_textid=# select * from output_candidates where variable_id='JOURNAL_13504@609' order by docid,varid,candid limit 20;
    variable_id    |     docid     | varid | candid | source | label |    candidate_id     |   id   | category | expectation | bucket |       word       |   random_number
-------------------+---------------+-------+--------+--------+-------+---------------------+--------+----------+-------------+--------+------------------+-------------------
 JOURNAL_13504@609 | JOURNAL_13504 |   609 |      0 | C      | f     | JOURNAL_13504@609_0 | 710987 |        1 |       0.018 |      0 | {inde-}          | 0.297377656213939
 JOURNAL_13504@609 | JOURNAL_13504 |   609 |      1 | T      | t     | JOURNAL_13504@609_1 | 682975 |        1 |       0.062 |      0 | {indeterminable} |  0.79233385482803
(2 rows)


# Order aware supv:

ddocr_100_textid=# select count(*), label from candidate group by label;
 count  | label
--------+-------
 702903 | f
 665654 | t


# 5gram supv:

...
...
..


# False example generation error

Found error: supervision FALSE example generation is WRONG
make the prediction lean towards false!

QUERY: 

    select docid, candidate_id, label, array_agg(word order by wordid) from candidate natural join cand_word group by docid, candidate_id,label,varid,candid order by docid, varid, candid;

Then error:

     JOURNAL_1001  | JOURNAL_1001@17_0     | f     | {www.elsevier.corn/locate/jseaes}
     JOURNAL_1001  | JOURNAL_1001@17_1     | t     | {www,.,e,|,sevier.com/locate/jseaes}

Because the script tried too hard to align..

This seems right:

    ddocr_100_textid=# select label,count(*) from candidate group by label;
     label | count
    -------+--------
     f     | 229300
           | 473603
     t     | 665654
    (3 rows)


TODO seems cand_2gram is not correct: (duplicated; why cand_word_id exists??)

ddocr_100_textid=# select * from cand_2gram limit 10;
     docid     |      cand_word_id       |     candidate_id      |        ngram
---------------+-------------------------+-----------------------+----------------------
 JOURNAL_26741 | JOURNAL_26741@10000_0.0 | JOURNAL_26741@10001_0 | St!ther(;hand. M.R..
 JOURNAL_26741 | JOURNAL_26741@10001_0.0 | JOURNAL_26741@10001_0 | St!ther(;hand. M.R..
 JOURNAL_26741 | JOURNAL_26741@10000_0.0 | JOURNAL_26741@10001_1 | St!ther(;hand. M.R.
 JOURNAL_26741 | JOURNAL_26741@10001_1.0 | JOURNAL_26741@10001_1 | St!ther(;hand. M.R.
 JOURNAL_26741 | JOURNAL_26741@10000_1.0 | JOURNAL_26741@10000_1 | Sutherland ,
 JOURNAL_26741 | JOURNAL_26741@10000_1.1 | JOURNAL_26741@10000_1 | Sutherland ,
 JOURNAL_26741 | JOURNAL_26741@10000_1.1 | JOURNAL_26741@10001_0 | , M.R..
 JOURNAL_26741 | JOURNAL_26741@10001_0.0 | JOURNAL_26741@10001_0 | , M.R..
 JOURNAL_26741 | JOURNAL_26741@10000_1.1 | JOURNAL_26741@10001_1 | , M.R.
 JOURNAL_26741 | JOURNAL_26741@10001_1.0 | JOURNAL_26741@10001_1 | , M.R.
(10 rows)


## Domain Ngram feature

doc_domain_1gram    40592033
doc_domain_2gram    DELETED
doc_domain_3gram    148877428

f_domain_2gram      2413934
f_domain_3gram      2747835

### Problem: seems to overfit the training set...

TODO: 
1. how many domain Ngrams are there in the TEST set?
    how to reduce this sparsity?
2. How to train a bag-of-word ngram? (may also overfit..)
3. This place word is X -> other place word is X (COREF!!)

    select variable_id, source, label, candidate_id, expectation, word, random_number from output_candidates where docid='JOURNAL_13504' order by varid,candid;