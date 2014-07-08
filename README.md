App: DeepDive OCR
====

### Put this repo under deepdive/app.

A DeepDive application on OCR systems.

Requirements
----

- PostreSQL
- Python
- Matplotlib (`pip install matplotlib`)

How to run the system
----

- Create a *ddocr* database (`createdb ddocr`)
- Change the application.conf `db.default.user` entry to yours.
- If necessary, add database connection details to `run.sh`
- Prepare your OCR output data, Google ngram data, distant supervision data.
- Execute `prepare_supv_data.sh` to load supervision data into database
- Execute `load_ngram_to_db.sh` to load Google Ngram data into database
- Do OCR Alignment by `script/AlignJournals.py`
- Execute `prepare_data.sh` to load aligned OCR outputs to databse.
- Execute `run.sh`.



Datasets
----

## Raw OCR Results

    140,982  /lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_JOURNAL
     43,487  /lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_feb15
     14,646  /lfs/madmax3/0/czhang/cleanpaleo/NLPRS_jan20_overlap.22/

## Candidates

    # /dfs/madmax3/0/zifei/deepdive/app/ocr/data/journals-output-new
    <!-- THIS IS WRONG!!! -->

    OR:
    /dfs/madmax/0/zifei/deepdive/app/ocr/data/journals-output

## Supervision HTMLs

first half:

    17,506  /dfs/madmax5/0/zifei/deepdive/app/ocr/data/sd-html/output-140508

second half:

    20,040  /dfs/madmax5/0/zifei/deepdive/app/ocr/data/output-secondhalf

or TOTAL:
    
    /dfs/hulk/0/zifei/ocr/sd-html/

## Escaped supervision / evaluation data:

How to prepare: (e.g.)

```bash
bash prepare_supv_data_from_html_xargs.sh eval /dfs/hulk/0/zifei/ocr/sd-html/ /dfs/hulk/0/zifei/ocr/evaluation_escaped_2/
```

    /dfs/hulk/0/zifei/ocr/supervision_escaped/
    /dfs/hulk/0/zifei/ocr/evaluation_escaped/

<!-- 
## Processed supervision data (bad escape)

    /dfs/madmax5/0/zifei/deepdive/app/ocr/data/supervision/
    OR 
    /dfs/madmax/0/zifei/deepdive/app/ocr/data/supervision/
    OR
    /dfs/hulk/0/zifei/ocr/supervision/

## Processed evaluation data (bad escape)

    /dfs/madmax5/0/zifei/deepdive/app/ocr/data/evaluation/
    OR 
    /dfs/madmax/0/zifei/deepdive/app/ocr/data/evaluation/
    OR
    /dfs/hulk/0/zifei/ocr/evaluation/
 -->

## Google Ngram
    /dfs/madmax/0/zifei/google-ngram/1gram/
    /dfs/madmax/0/zifei/google-ngram/2gram/
    OR
    /dfs/madmax5/0/zifei/deepdive/app/ocr/data/google-ngram/1gram/
    /dfs/madmax5/0/zifei/deepdive/app/ocr/data/google-ngram/2gram/
    OR 
    /dfs/hulk/0/zifei/ocr/google-ngram/1gram/
    /dfs/hulk/0/zifei/ocr/google-ngram/1gram.tsv
    /dfs/hulk/0/zifei/ocr/google-ngram/2gram_reduced.tsv

## Web Ngram (filtered by 10000)

    /dfs/hulk/0/zifei/ocr/web_ngram/3gram.tsv
    /dfs/hulk/0/zifei/ocr/web_ngram/4gram.tsv
    /dfs/hulk/0/zifei/ocr/web_ngram/5gram.tsv

## Domain corpus (HTML aggregated by docid)

    /dfs/hulk/0/zifei/ocr/domain-corpus/domain-corpus.tsv

<!-- /dfs/madmax3/0/ -->


## KB data

    /dfs/hulk/0/zifei/ocr/kb/intervals.tsv
    /dfs/hulk/0/zifei/ocr/kb/paleodb_taxons.tsv
    /dfs/hulk/0/zifei/ocr/kb/supervision_occurrences.tsv

    # Aggregated:
    /dfs/hulk/0/zifei/ocr/kb/entity_kb.tsv
    /dfs/hulk/0/zifei/ocr/kb/entity_kb_words.txt

    # ngrams
    /dfs/hulk/0/zifei/ocr/kb/domain_1gram_100docs_reduced5.txt
    /dfs/hulk/0/zifei/ocr/kb/domain_1gram_100docs.txt
    /dfs/hulk/0/zifei/ocr/kb/google_1gram_1000.txt
    /dfs/hulk/0/zifei/ocr/kb/google_1gram_10k.txt


Ground truth
----

HTML: (hold out 1/5 as ground truth and rest for distant supervision; run 5 times to make sure they do not differ wildly...)

    168,790  /lfs/madmax3/0/czhang/cleanpaleo/jid2url.tsv

     37,545  grep sciencedirect /lfs/madmax3/0/czhang/cleanpaleo/jid2url.tsv
     

     priority: 
     1. /lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_feb15/[JID] 
     2. /lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_JOURNAL/[JID] 



Dependencies
----

- python-Levenshtein
- pyquery
- snappy 0.8.5 or higher (http://snap.stanford.edu/snappy/0.8.5/)
- psql "fuzzystrmatch" module: 
    - http://blog.2ndquadrant.com/wp-content/uploads/2011/03/fuzzystrmatch-gp-4.0.4.0.tar.gz
    - Doc: http://blog.2ndquadrant.com/fuzzystrmatch_greenplum/
- psql "pg_trgm" module (in GiST):
    - http://www.sai.msu.su/~megera/postgres/gist/pg_trgm/pg_trgm.tar.gz
    - Docs: http://www.sai.msu.su/~megera/postgres/gist/