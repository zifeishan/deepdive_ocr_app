OCR Error analysis
===================

## Protocol
```bash
grep 'JOURNAL_13504' /tmp/ocr-output-words.tsv | cut -f 3 > tmptmp
vimdiff tmptmp /dfs/hulk/0/zifei/ocr/evaluation/JOURNAL_13504.seq
```

Also use:
`diff tmptmp /dfs/hulk/0/zifei/ocr/evaluation/JOURNAL_13504.seq | grep '^>' | wc -l`
as nominator...

TODO

## Errors
Many: escaping errors

Many: (won't reflect, precision errors, but should fix)
- caused by missalignment!

      maximum                                                                                  |  maximum
      mum                                                                                      |  ----------------------------------------------------------------------------------------

    Avenay                                                                                   |  Avenay
      nay                                                                                      |  ----------------------------------------------------------------------------------------


`upp` feature seems not working well. `Frank` got one...


Adding domain ngram
----
ddocr_100_new=# select count(*) from domain_1gram;
  count
---------
 1796997
(1 row)

ddocr_100_new=# select count(*) from domain_2gram;
  count
----------
 19474013
(1 row)

ddocr_100_new=# select count(*) from domain_3gram;
  count
----------
 60657016
(1 row)