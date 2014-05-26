  May 26:
  - run pipeline with TEXT ids
  - compare order aware supervision
  - is new learning problem because of the "each" ngram feature? why?

  - if FE takes too long, try on a 30 dataset...

  - ERROR ANALYSIS with gnu diff! 
  - See what's the feature needed!

  OCR: 
  - Change plot to Err Red rates
  - Figure out whether it's supervision / feature problem
    - (what's the plot like when supervised with optimal labels?)


  OCR: 
  - TUNE ngram feature COUNT parameter
X - PLOT comparisons with T/C/Best (evaluation/plot-*.py)


  Write script: generate 2gram
  Backup order-aware supv result

  orderaware: 343 docs extracted; 60 docs not extracted (for eval!) 

X Evaluate all OCR results: (experiment)

    bash generate_all_ocr_results.sh ddocr
  OR: (after getting /tmp/...)
    pypy ocr-evaluation-strict.py /tmp/ocr-output-words-tesseract-all.tsv data/test-evaluation/ eval-results-tess-all.txt

- 

X  python load_supervision_data_from_list.py ddocr_1k /lfs/local/0/zifei/deepdive/app/ocr/data/evaluation/ ../data/doclist-1k.txt

/ try fuzzy matching (in [:10]?)

* Write a general script to label with Ngram, used for both and!
    Infolab Physical cores: Cores / 2.

X DEBUG order aware supervision. 
/   Test dirty cases?

* Add NLP features
/ Run on larger dataset

X Why does constraint increast T weight? (AND is ok)

X why copy to tsv do not include all words??

X WHY not all variables? --ANSWER: evidence!
    
    ddocr=# select * from candidate_label_inference order by docid,varid limit 10;

DONE less than 1000 supv data; fix cases where words too few! (not real supv data)

--

Fix after scripts?

OCR New idea: (CE)
- How do fonts change from time?
- Can we build a model to capture font changes, and use today's data to train previous ones?


AI2:
- Waffman Alpha
- See how Watson win the test. Can Watson do AI2?
- Set up break Plan!


Get supervision numbers:
1. #examples of each, and quality
2. conflicts?

Deal with mul words in a (T) box:

  13474 |       | JOURNAL_107511 |    248 |      1 | T      | Bipedalism
  13475 |       | JOURNAL_107511 |    248 |      2 | T      | ;


Removed rows in document JOURNAL_102371.

  Move alignment to Extractors?

  Feature engineering extractors?
    Naive features
    Ggl ngram
    paleo gram?

/ Supervision
X   1gram
    2gram (pluggable)

  Evaluation
    hand-crawl
    order-aware script!

  - Put everything in extractors
X - Implement new alignment by bounding boxes
  - Generate a list with supervision data
  - import all files in the list


Fix error in Combiner.py: TODO!!


Schema design:

OCR(id, ocrid, docid, word) 
- get from input.text / fonts.text

OCR_box(id REFERENCES OCR(id), page, left, top, right, bottom)
- get from ???

OCR_sentence(id REFERENCES OCR(id), sentid, wordid)
- get from ???
- e.g. word a: sent 17, word 6

word(id, docid, wordid, word?)
- get from "docid.word"?
- do not need now?

candidate(id, word.id REFERENCES word(id), ) ???
- do we create foreign keys??

candfeature(id, cand.id, ocrid, distance) ???

feature(id, word.id, fname, fval)


