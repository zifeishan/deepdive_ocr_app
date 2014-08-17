Aug 9

What takes long:
  - alignment: 10-30s / doc (?)
  - preprocessing domain corpus (~20min regardless of #docs)
  - candidate generation (1-20min for a doc, depends on #words)

  - DFS (should be improved!!)


Jul 29
doc100:madmax
doc30: madmax2

6622567 candidates
was not using correct supv...

CLEAN

zifei@madmax: ocr (master) $ python plotting/plot-candgen-bestpick.py
Usage: plotting/plot-candgen-bestpick.py tesspath cunipath optimalpath ddpath. Used default.
Plotting 24 documents
Plot saved to:  pick-result.eps
tess avg    : 0.92443
dd(ens) avg : 0.93422
opt avg     : 0.93858
dd(gen) avg : 0.93140
opt(gen) avg: 0.95638
opt(1) avg  : 0.94959
opt(2) avg  : 0.96397
ErrRed tess -> dd(ens) : 0.13081
ErrRed tess -> dd(gen) : 0.09000
ErrRed opt -> opt(gen) : 0.28798
ErrRed tess -> opt(gen): 0.42519


DIRTY

tess avg    : 0.84222
dd(ens) avg : 0.85851
opt avg     : 0.86662
dd(gen) avg : 0.85851
opt(gen) avg: 0.88093
opt(1) avg  : 0.89592
opt(2) avg  : 0.90431
ErrRed tess -> dd(ens) : 0.10349
ErrRed tess -> dd(gen) : 0.10349
ErrRed opt -> opt(gen) : 0.10473
ErrRed tess -> opt(gen): 0.24423

X TODO: erranal for opt(2)

TODO:
  - rerun pipeline for both datasets
  - generate a report for Ce (if needed, more error analysis)
  - 3gram features?

TODO 
  done reescaping html,
  removed highlights section,
  check and move results in /dfs/rambo/0/zifei/ocr/evaluation_escaped_tmp/

0.93710 after escaping remove highlights...

Jul 26:

Added editops feature & correct dist feature:

ddocr_100_candgen:

    tess avg    : 0.92443
    dd(ens) avg : 0.93422
    opt avg     : 0.93812
    dd(gen) avg : 0.93709
    opt(gen) avg: 0.94996
    opt(1) avg  : 0.94959
    opt(2) avg  : 0.95697
    ErrRed tess -> dd(ens) : 0.13081
    ErrRed tess -> dd(gen) : 0.16841
    ErrRed opt -> opt(gen) : 0.19077
    ErrRed tess -> opt(gen): 0.34016

ddocr_dirty:

    tess avg    : 0.80001
    dd(ens) avg : 0.81429
    opt avg     : 0.81653
    dd(gen) avg : 0.81429
    opt(gen) avg: 0.83956
    opt(1) avg  : 0.83231
    opt(2) avg  : 0.86594
    ErrRed tess -> dd(ens) : 0.08585
    ErrRed tess -> dd(gen) : 0.08585
    ErrRed opt -> opt(gen) : 0.15517
    ErrRed tess -> opt(gen): 0.23749

(dirty) Only English, 20 docs: 

    tess avg    : 0.84222
    dd(ens) avg : 0.85851
    opt avg     : 0.86188
    dd(gen) avg : 0.85851
    opt(gen) avg: 0.88093
    opt(1) avg  : 0.87953
    opt(2) avg  : 0.89516
    ErrRed tess -> dd(ens) : 0.10349
    ErrRed tess -> dd(gen) : 0.10349
    ErrRed opt -> opt(gen) : 0.13906
    ErrRed tess -> opt(gen): 0.24423

Jul 25

Running:
  - madmax: doc100
  - madamx2: dirty
check for editops results!!

  wordlen + source?
  logcount x ratio?
  wordlen x ratio + source?

/ TODO before comb: escaping wrong?

!!!! TODO: edit distance feature: "what edit is it?"
  - insert a "-" is so cheap
  - ? -> fi is cheap, etc.
  - each edit is a feature.
  - this seems the correct way to do things!
  - use "Levenshtein.editops":

    In [4]: Levenshtein.editops('addhoc', 'add-hoca')
    Out[4]: [('insert', 3, 3), ('insert', 6, 7)]

#### Feature engineering for dd(gen):

    original:       0.93572
    remove constraint, add two dist features: 0.93471
    added char2:    0.93480
    add paleo:      0.93446
    add dist ratio: 0.93509
    add constraint: 0.93622
    add editops:    0.93709

X TODO check result for "ratio" feature

TODO:
1. opt(gen) -> opt(2) fixes
2. Plot for dirty documents
3. error analysis to improve dd(gen)!

before adding gen4valid:
  INFO  # nvar               : 3708372
  INFO  # nfac               : 53558995
  INFO  # nweight            : 1233
  INFO  # nedge              : 70432679
after adding gen4valid:
  INFO  # nvar               : 6572335
  INFO  # nfac               : 115445957
  INFO  # nweight            : 1434
  INFO  # nedge              : 164754823
removed constraint:
  INFO  # nvar               : 6572335
  INFO  # nfac               : 68028072
  INFO  # nweight            : 1439
  INFO  # nedge              : 68028072




Jul 24

X now running all tesseracts... why number higher than ours?
X now running if already have existing cands...
  - takes much longer..

    tess avg    : 0.92443
    dd(ens) avg : 0.93422
    opt avg     : 0.93812
    dd(gen) avg : 0.93572
    opt(gen) avg: 0.94839
    opt(1) avg  : 0.94959
    opt(2) avg  : 0.95697
    ErrRed tess -> dd(ens) : 0.13081
    ErrRed tess -> dd(gen) : 0.14767
    ErrRed opt -> opt(gen) : 0.16209
    ErrRed tess -> opt(gen): 0.31666

X TODO:

X 1. OMG Just rerun the candgen, the "lang" error can be fixed!! (because of trie bug)
X 2. finish the email
X 3. find documents that (1) has long .seq in EVAL_DIR (2) is DIRTY!!


  - refpunc
X - "language"?? direct a->a`? coreference? other "CT" cands for candgen??
  - add simple "direct", 
X - ---rerun candgen totally!! changed trie.py!!

Jul 23

Why is there a gap betw/ current opt(x) and previous:
- now we only generate for "words" (at least 1 English letter)

tess avg    : 0.92443
dd(ens) avg : 0.93422
opt avg     : 0.93812
dd(gen) avg : 0.93629
opt(gen) avg: 0.94666
opt(1) avg  : 0.95035
opt(2) avg  : 0.95873
ErrRed tess -> dd(ens) : 0.13081
ErrRed tess -> dd(gen) : 0.15740
ErrRed opt -> opt(gen) : 0.13760
ErrRed tess -> opt(gen): 0.29616

Jul 22

tess avg    : 0.92443
dd(ens) avg : 0.93422
opt avg     : 0.93812
dd(gen) avg : 0.93629
opt(gen) avg: 0.94666
opt(1) avg  : 0.94057
opt(2) avg  : 0.94242
ErrRed tess -> dd(ens) : 0.13081
ErrRed tess -> dd(gen) : 0.15740
ErrRed opt -> opt(gen) : 0.13760
ErrRed tess -> opt(gen): 0.29616

TODO:
X 1. add dd ensemble results
! 2. add dirty documents
  3. err ana

     --------------------------------------------------
     Summary Report
     --------------------------------------------------
     ext_eval_opt1 SUCCESS [215342 ms]
     ext_eval_opt2 SUCCESS [554269 ms]
     ext_eval_opt3 SUCCESS [1044646 ms]
     --------------------------------------------------
     Completed task_id=report with Success(Success(()))

Fix: KB trie with codecs...

FATAL: fix trie.py numcands! should rerun candgen totally!

Try new method to generate opt(1): 
X - use ground truth as KB
X - X-axis sorted by Tess
X - 蓝线不是正常的protocol生成出来的
X - dd-ensemble的线画上去
! - 为什么不能用最开始error analysis过的两个doc做？
  - 

TODO!!! Tesseract too clean.
  - Compare with former err anal
TODO!!! run dd without generation

TODO: Check gap between opt(gen) and opt(2) rather "trans"

TODO: first "verify" candidates in KB, then only gen for unverified candidates..?
TODO: write a sql script to check a certain word's generated candidates?
TODO: char 2gram feature for T/C (initial bias)

Jul 21

X Seems working well! Check plot results. Generate numbers for Ce.

    tess avg    : 0.92443
    dd avg      : 0.93629
    opt avg     : 0.93812
    opt(gen) avg: 0.94666
    opt(1) avg  : 0.95984
    ErrRed tess -> dd      : 0.15740
    ErrRed opt -> opt(gen) : 0.13760
    ErrRed tess -> opt(gen): 0.29616

! Give evaluation protocol.

X  (solved) Bottleneck: cannot run DP on huge generated candidates...
    (because N1*N2 is long long rather than int in C++.)

When N1*N2 =10k * 2k: 6min for 2 docs (2 parallel):

    09:07:24 INFO  JOURNAL_58762 Running DP.. N1=86197, N2=24305
    09:07:24 INFO  JOURNAL_58568 Running DP.. N1=93406, N2=24076
    ext_sup_orderaware_incremental SUCCESS [364666 ms]

Stats:

    ddocr_100_candgen=# select source, count(*) as cnt from cand_word where docid='JOURNAL_58568' group by source order by cnt desc;
                source             |  cnt
    -------------------------------+-------
     CSeg_Presg                    | 19009
     T                             | 18826
     C                             | 17232
     T_PaleoSg                     | 14762
     CT_PaleoSg                    | 12394
     C_PaleoSg                     |  7267
     CT                            |  4967
     C_GglSg                       |  3524
     CComb_Presg                   |  3100
     T_GglSg                       |  2910
     TSeg_Presg                    |  1618
     TComb_Presg                   |  1430
     ...


Speed based on seg/comb (dist 2, maxcands 3, comb20, seg5):

  domain: 5 docs / min

Added segcomb candgen. distance need to be treated individually?


    Plotting 24 documents
    Plot saved to:  pick-result.eps
    tess avg  : 0.9244
    dd avg    : 0.9338
    opt avg   : 0.9381
    opt(1) avg: 0.9598
    Avg Error reduction from Tesseract: 0.123978876371
    Avg Error reduction from Optimal: -0.0745110389621

Testing match of Tesseract:

    test/match_tesseract_with_docid.sh JOURNAL_13504
    Saved to test/tess-output/JOURNAL_13504.seq
    Matching Tesseract with sequence using original stringmatch:
    pypy candmatch.py test/tess-output/JOURNAL_13504.seq /dfs/hulk/0/zifei/ocr/evaluation_escaped/JOURNAL_13504.seq
    2038

    zifei@madmax: util (master) $ pypy candmatch.py test/tess-output/JOURNAL_13504.seq /dfs/hulk/0/zifei/ocr/evaluation_escaped/JOURNAL_13504.seq
    2039


    zifei@madmax: util (master) $ pypy candmatch_eval.py test/tess-output/JOURNAL_13504.seq /dfs/hulk/0/zifei/ocr/evaluation_escaped/JOURNAL_13504.seq
    2039

Jul 18

Error reduction: 
- talk about absolute precision

- Monday: make sure numbers are correct

- order-aware

FATAL: Is our C++ DP script correct? Test two sequences with seqmatch / candmatch!


Error analysis:

    author  37  33.94%
      - Author name in citation mismatch
    seg 25  22.94%
      - segmentation
    direct  13  11.93%
      - need "confusion matrix" for candidate generation (rm->nn)
    ??  9 8.26%
      - not sure how to fix
    comb  7 6.42%
      - combination
    char  6 5.50%
      - non-ascii characters have different representations (-, ", ~, ...)
    lan 4 3.67%
      - a different language
    comb, char  3 2.75%
      - combination + character

TODO:

  - Remove "intra_ref" in HTML for evaluation

"? -> fi" cannot be fixed in dist 1...

    TODO Removed 'Sum&agrave;rio' and rerun

X   TODO rewrite evaluation script in C++

Jul 17

Rerun again:

X   mv /dfs/hulk/0/zifei/ocr/evaluation_escaped/ /dfs/hulk/0/zifei/ocr/evaluation_escaped_old2/

X   mv /dfs/hulk/0/zifei/ocr/evaluation_escaped_2/ /dfs/hulk/0/zifei/ocr/evaluation_escaped/

X Then rerun all evaluations......

X TODO: check results in :

    /lfs/local/0/zifei/bestpick-evalgen/
    /lfs/local/0/zifei/bestpick-result/


Jul 16

TODO run checkgen.sh for more docs (prior wrong)

JOURNAL_13730

All-dist1:

    Avg Error reduction from Tesseract: 0.122515117947
    Avg Error reduction from Optimal: -0.0471327074561

TODO a simple way: 

Before candgen, NO kb, only do seg/comb within a single var.
May combine C/T into a "CT"?

Combination is important!!

TODO: PaleoSg too stupid: do not have basic dictionary. Only gen for "unrecognized" ones?

Jul 15

TODO Combine multiple candgen results
Then see errors again...

TODO feature: (different) KB verification


Jul 14

JOURNAL_45405:
- Most errors are: OCR tokenization errors
- TODO: tokenize Cuneiform before Align.py !!!

TODO Cuneiform fixes:
- TODO: combine 'xxx-' + 'yyy' (nextline)
- TODO: 'geological' 'logical'

Jul 10

TODO get opt(gen) results in: /lfs/local/0/zifei/bestpick-evalgen/

New eval (domain 1gram):

    Avg Error reduction from Tesseract: 0.136012780223
    Avg Error reduction from Optimal: -0.0325676481956


TODO rerun all evaluation

  < 22% error reduction: not so much...

X TODO error: 
    Keyword section mismtach? (might have been fixed by removing Resume)

X HTML escaping:

X Divs to remove:
    - Resume (not English)
    - Copyright (not in original doc)

TODO: 
    
X   rm -rf /dfs/hulk/0/zifei/ocr/evaluation_escaped/

X   mv /dfs/hulk/0/zifei/ocr/evaluation_escaped_2/ /dfs/hulk/0/zifei/ocr/evaluation_escaped/


<div class="artFooterContent"><dl class="correspondence" id="cor1"><dt class="label topPadd"><a href="#bcor1" class="intra_ref"><sup><img class="imgLazyJSB" border="0" src="http://cdn.els-cdn.com/sd/entities/REcor.gif" alt="Corresponding author contact information" title="Corresponding author contact information" data-inlimg="/entities/REcor.gif" data-loaded="true" style="display: inline;"><noscript>&lt;img border="0" alt="Corresponding author contact information" title="Corresponding author conact information" src="http://origin-cdn.els-cdn.com/sd/entities/REcor.gif"&gt;</noscript></sup></a></dt><dd>Corresponding author.</dd></dl><!--footerNotes--></div>

<p class="copyright">Copyright © 2010 Académie des sciences. Published by Elsevier Masson SAS All rights reserved.</p>

TODO future:
  (Optional) minimizing edit distance rather than maximizing #matches in supervision?


Jul 8


TO STUDY:

      - "at most generate K new candidates for one original word (K=5 in these experiments);"
      - K=1,2,3,4,5...infinity, what about quality change??

Tables

    generated_cand_word_google_1gram
    orderaware_supv_label_google_1gram

  Features:
    - "best candidate": with minimum distance
    - single best candidate: the only one with minimum distance
    - wordlength: 1/2/3/.../6/ / many

  TODO: 
  following Errors:
  'darl <' -> 'dark'
  'cl' -> 'd'
    - Confusion matrix?
    - 2gram?

  Findings:
  3 candidates are enough
  Most words are correct (10k KB too small?)

Avg Error reduction from Tesseract: 0.109664184133
Avg Error reduction from Optimal: -0.0357580202109
+onebset:

Avg Error reduction from Tesseract: 0.105452891665
Avg Error reduction from Optimal: -0.0404587545291
+ multi:
10.3

Domain Ngram:
0.116417383854
-0.0285583842851

Jul 7

X TODO: Get "why is opt(1) so high": fuzzy match that counts "match 
  results" stats.

  TODO: OCR confusion matrix! error probability, weighted matrix

  TODO: bigram language model


X GET SUPERVISION STATS:

    select source, label, count(*) from candidate group by source, label order by source, label;

X Benchmarks: KB dist 1 (~= without candgen)

    Avg Error reduction from Tesseract: 0.0948142717848
    Avg Error reduction from Optimal: -0.0545531954891

X How to get optimal bound for generated candidates:

    rm -f /lfs/local/0/zifei/bestpick-result-candgen-dict/*

    export BESTPICK_DIR='/lfs/local/0/zifei/bestpick-result-candgen-dict/'
    ./run-bestpick.sh

    cat /lfs/local/0/zifei/bestpick-result-candgen-dict/*.stat.0 > evaluation/bestpick-candgen-kb-100.txt

    python plotting/plot-candgen-bestpick.py



  Jul 4
X - "words" -> CandGen(' '.join(words)), not most systematic

Time: 1634.545 ms
ddocr_100_candgen=# select CHAR_LENGTH(word) as wordlen, count(*) from cand_word where source like '%Sg' group by wordlen order by wordlen;
 wordlen |  count
---------+---------
       1 | 1086260
       2 |  573563
       3 |  238916


    19:26:16 [extractorRunner-ext_sup_orderaware] INFO  JOURNAL_57921 ERROR: lengths does not match! / Empty data!
    19:26:17 [extractorRunner-ext_sup_orderaware] INFO  JOURNAL_58568 ERROR: lengths does not match! / Empty data!
    19:26:17 [extractorRunner-ext_sup_orderaware] INFO  JOURNAL_58670 ERROR: lengths does not match! / Empty data!
    19:26:17 [extractorRunner-ext_sup_orderaware] INFO  .JOURNAL_58762 ERROR: lengths does not match! / Empty data!
    19:26:17 [extractorRunner-ext_sup_orderaware] INFO  JOURNAL_63084 ERROR: lengths does not match! / Empty data!

  STATS:
  1. generate 1x--5x more candidates
  2. 

  MAJOR PROBLEMS:
  1. Do we need to generate candidates when one of the candidates are "valid"??
    - yes and?
    - do experiments on evaluation
  2. How to deal with short words?

['2'] 52 [('A', 1), ('C', 1), ('B', 1), ('E', 1), ('D', 1), ('G', 1), ('F', 1), ('I', 1), ('H', 1), ('K', 1)]
['1'] 52 [('A', 1), ('C', 1), ('B', 1), ('E', 1), ('D', 1), ('G', 1), ('F', 1), ('I', 1), ('H', 1), ('K', 1)]
['2'] 52 [('A', 1), ('C', 1), ('B', 1), ('E', 1), ('D', 1), ('G', 1), ('F', 1), ('I', 1), ('H', 1), ('K', 1)]
['2'] 52 [('A', 1), ('C', 1), ('B', 1), ('E', 1), ('D', 1), ('G', 1), ('F', 1), ('I', 1), ('H', 1), ('K', 1)]
['lc'] 7 [('c', 1), ('l', 1), ('la', 1), ('lac', 1), ('li', 1), ('lo', 1), ('ly', 1)]
['dnl'] 1 [('dal', 1)]
['.'] 52 [('A', 1), ('C', 1), ('B', 1), ('E', 1), ('D', 1), ('G', 1), ('F', 1), ('I', 1), ('H', 1), ('K', 1)]
['<'] 52 [('A', 1), ('C', 1), ('B', 1), ('E', 1), ('D', 1), ('G', 1), ('F', 1), ('I', 1), ('H', 1), ('K', 1)]
['.'] 52 [('A', 1), ('C', 1), ('B', 1), ('E', 1), ('D', 1), ('G', 1), ('F', 1), ('I', 1), ('H', 1), ('K', 1)]

  Jul 2
/ - Trigram similarity: error analysis
    - TODO: Why trigrams implemented as '$$word$' + LOWER?
    - Refer to: http://www.sai.msu.su/~megera/wiki/ReadmeTrgm
  - TODO gather result for analysis.

  Jul 1
  - General-purpose KB
    - English dict
    - Freebase?
    - Wikipedia?

    select word, name, word <-> name from cand_word, entity_kb where word % name order by word<->name limit 10;

  deprecated: Get "non-dict" words to generate candidates (or too many canditates?)

  ERROR ANALYSIS for current candgen (why bad?)

  Write evaluation script with C++

  TODO (Jun 19): now can run with 3000-subsample. Let's run with more cand gen. (KB!) KB address:
    /Users/Robin/ssh-afs-deepdive/app/ocr/data-local

X TODO: supervision too slow. force alignment? subsample?
  - implemented with C++!
    
    NEW
    INFO  [JOURNAL_18178]  SCORE: 3569 / 5151 (0.692875), matches: 3569 / 8900
    OLD
    DEBUG DOCID: JOURNAL_18178  MATCHES: 3278 / 5151 (0.6364)

  TODO: make sure candgen plot makes sense by looking at "THE MATCHED WORDS"!!

  TODO: Add KB. 
  (entity and relation applies below:)
    https://raw.githubusercontent.com/zhangce/cleanpaleo/master/dicts/supervision_occurrences.tsv

    https://raw.githubusercontent.com/zhangce/cleanpaleo/master/dicts/paleodb_taxons.tsv

    https://raw.githubusercontent.com/zhangce/cleanpaleo/master/dicts/intervals.tsv

/ TODO: debug orderaware 
    SUPV_DIR=/dfs/hulk/0/zifei/ocr/supervision_escaped/ pypy udf/ext_sup_orderaware.py </tmp/ext_sup_orderaware.input

  - We CAN do a DP over lattice same as SPEECH, without changing data tables! Just a different way of building graphs ("edges" table)...

  TODO: parameter space for candidate generation

X DONE: Spell corrector with non-alphabet chars..! UTF8! Domain corpus!
  - 100 docs:
  - 20-thread parallel with pypy
  - 180 seconds
  - 96050 new candidates (119618 new cand words)

? Spell slides say: “80% of errors are within edit distance 1
  Almost all errors within edit distance 2”


  STEPS:
X 1. generate a candidate that appears in this document by edit distance
  2. generate a candidate that appears in domain corpus by edit distance
  3. splits / combines / ...

Talked with Chris: Candidate generation

1. knowledge base as a dictionary (Lexical & syntactic features)
2. cooccurence statistics: 
  - fixing two Nouns / NPs, what's the bag of words between them?
  - fixing a word sequence (pattern; is married to, etc), what's the thing at the two ends?


## FUTURE:
- add Latin parser
- add stanford parser + "FW" -> Latin word / *Italic font*

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


