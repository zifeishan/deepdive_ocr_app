  Move alignment to Extractors?

  Feature engineering extractors?
    Naive features
    Ggl ngram
    paleo gram?

  Supervision
    1gram
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


