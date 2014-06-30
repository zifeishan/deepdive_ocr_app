# Error analysis: reproduce

## NEW (textid)
14:22:45 [sampler] INFO  # nvar               : 1368557
14:22:45 [sampler] INFO  # nfac               : 10031808
14:22:45 [sampler] INFO  # nweight            : 73
14:22:45 [sampler] INFO  # nedge              : 10733424

### Rules

    "f_naivefeature",
    "f_constraint",
    # "f_nlp_pos",
    # "f_nlp_ner",
    "f_ocr_bias",
    "f_1gram_pos",
    "f_1gram_neg",
    "f_2gram_somepos",
    "f_2gram_allneg",
    # "f_2gram_someneg", # same as somepos....
    "f_2gram_allpos",
    "f_2gram_each", # new one

 count  | label
--------+-------
 290556 | f
 560313 | t

ddocr_100_textid=# select * from dd_inference_result_variables_mapped_weights order by weight asc limit 10;
 id | initial_value | is_fixed |        description         |      weight
----+---------------+----------+----------------------------+-------------------
  3 |             0 | f        | f_ocr_bias-C               | -24.6915765696104
  1 |             0 | f        | f_ocr_bias-T               | -21.8043041504408
  2 |             0 | f        | f_ocr_bias-CT              | -20.4915370293978
  4 |           -20 | t        | f_constraint-              |               -20
  5 |             0 | f        | f_2gram_allneg-            | -19.5325037285703
 34 |             0 | f        | f_naivefeature-notascii_CT | -3.54519667817865
 21 |             0 | f        | f_naivefeature-!_T         | -3.07956040042928
 18 |             0 | f        | f_naivefeature-!_C         | -3.04190713852944
  9 |             0 | f        | f_naivefeature-'_C         | -1.70094878859205
 13 |             0 | f        | f_naivefeature-,_C         | -1.66215790797251
(10 rows)

### supervision

 ddocr_100_textid=# select count(*), source, label from candidate group by source, label order by source, label;

 count  | source | label
--------+--------+-------
 415519 | C      | f
  48354 | C      | t
 118350 | CT     | f
 388875 | CT     | t
 169034 | T      | f
 228425 | T      | t
(6 rows)

### Fixed rule

select count(*), c1.label, c2.label from candidate as c1, candidate as c2 where c1.docid = c2.docid AND c1.variable_id = c2.variable_id and c1.candidate_id != c2.candidate_id group by c1.label,c2.label;

 count  | label | label
--------+-------+-------
 229300 | f     | t
 243016 | f     | f
 229300 | t     | f
(3 rows)


### Old (int id)
INFO  # nvar               : 1368557
INFO  # nfac               : 13618140
INFO  # nweight            : 161
INFO  # nedge              : 14319756
15:06:05 [sampler] INFO  ################################################
15:06:06 [sampler] INFO  LOADED VARIABLES: #1368557
15:06:06 [sampler] INFO           N_QUERY: #322646


ddocr_100_new=# select * from dd_inference_result_variables_mapped_weights order by weight asc limit 10;
 id  | initial_value | is_fixed |  description  |      weight
-----+---------------+----------+---------------+-------------------
 147 |             0 | f        | f_nlp_ner-    | -69.3606318103204
  96 |             0 | f        | f_nlp_pos-,   | -30.9984849317056
  78 |             0 | f        | f_nlp_pos-NNP | -30.5803573524818
 100 |             0 | f        | f_nlp_pos-DT  | -23.6386938681226
  61 |           -20 | t        | f_constraint- |               -20
 145 |             0 | f        | f_nlp_ner-JJ  | -19.7122484625103
 103 |             0 | f        | f_nlp_pos-CD  | -18.5260109209221
   1 |             0 | f        | f_1gram_neg-  | -18.3176056139124
  75 |             0 | f        | f_nlp_pos-NN  | -17.8775531654539
 101 |             0 | f        | f_nlp_pos-.   | -16.7155757118854
(10 rows)

ddocr_100_new=# select * from dd_inference_result_variables_mapped_weights order by weight desc limit 10;
 id  | initial_value | is_fixed |     description     |      weight
-----+---------------+----------+---------------------+------------------
  70 |             0 | f        | f_nlp_pos-          |  47.995667123723
 108 |             0 | f        | f_1gram_pos-        | 17.6046550714247
 142 |             0 | f        | f_nlp_ner-,         |  11.913120517846
 121 |             0 | f        | f_nlp_ner-NNP       | 10.8020002171747
   0 |             0 | f        | f_2gram_allneg-     | 8.59464350636247
   3 |             0 | f        | f_ocr_bias-CT       | 7.29483236001661
   2 |             0 | f        | f_ocr_bias-T        |  5.6076401658588
   4 |             0 | f        | f_ocr_bias-C        | 5.37059699845633
 136 |             0 | f        | f_nlp_ner-DT        | 4.98419332758014
  58 |             0 | f        | f_naivefeature-fi_C | 2.44177321864295
(10 rows)