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
- Execute `run.sh`



Datasets
----

    140,982  /lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_JOURNAL
     43,487  /lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_feb15
     14,646  /lfs/madmax3/0/czhang/cleanpaleo/NLPRS_jan20_overlap.22/



Ground truth
----

HTML: (hold out 1/5 as ground truth and rest for distant supervision; run 5 times to make sure they do not differ wildly...)

    168,790  /lfs/madmax3/0/czhang/cleanpaleo/jid2url.tsv

     37,545  grep sciencedirect /lfs/madmax3/0/czhang/cleanpaleo/jid2url.tsv
     

     priority: 
     1. /lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_feb15/[JID] 
     2. /lfs/madmax3/0/czhang/cleanpaleo/TORUNEXT_JOURNAL/[JID] 

