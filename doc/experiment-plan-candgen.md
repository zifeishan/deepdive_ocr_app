Similarity Measure
====

## Edit distance

- Our last experiment justifies edit distance measure:
  - About 30--50% errors are within edit distance 1. 
    - This means that, if all possible candidates within edit distance 1 to OCR outputs are generated, we can reduce 30--50% errors from an "optimal" system that selects the correct answer from OCRs.
  - About 50--70% errors are within edit distance 3.

(Figure)

TODO give exact numbers for error reduction rate for opt(X), X=1..5

## Other possible measures

- Trigram similarity / distance
  - For string x and y, TX / TY is the bag of trigrams of x / y, sim(x, y) is the Jaccard similarity of TX and TY; dist(x, y) is the Jaccard distance of TX and TY.

TODO other measures?


Candidate generation Experiments
====

## General-purpose KB (entity level)

Hypothesis: using a general-purpose KB to generate candidates will cover most errors OCR make.

### Protocol

- Potential KB to use:
  - English dictionary 
  - Freebase entities
  - WordNet
  - ConceptNet
  - Wikipedia

- Implementation:
  1. Init KB in database, which is a set of strings (valid candidates to generate).
  2. Candidate generation: 

    - (Possible method 1) given a string s in OCR output (that may be composed by one or multiple adjacent words), find another string s' in KB, s.t., dist(s, s') < threshold.
  
    - (Possible method 2) given a word in OCR output, find another string s' in KB, s.t., dist(s, s') < threshold.  Assumption here is that OCR segmentation is correct, which is not always true.

  3. Extract features for generated candidates (e.g. dist)
  4. Run learning and inference
  5. Evaluation

### Proxy: how to evaluate hypothesis

Calculate recall on evaluation document set. Compare it to:
- system recall without candidate generation (dd)
- optimal recall of selecting from one OCR output (opt_0)
- optimal recall of selecting from all generated candidates (opt_candgen)
  - To get the system well calibrated, "dd" should approach "opt_candgen".
- optimal recall of selecting from all possible candidates within edit distance X (opt_X)
  - If there's a gap to its according line in opt_X, it shows that we need a better KB. 

### Expected result

Generating candidates within edit distance X using a general-purpose KB, Line "dd" should go above opt_0 (at least slightly), but it can never go higher than opt_X.

We expect that there is a large gap between dd and opt_X. To fill this gap, we need to do error analysis. Hopefully most errors can be covered by using a domain-specific KB.

### Next step

If error analysis shows that domain-specific KB helps, we will implement candidate generation with domain-specific KB.

Otherwise we will fix errors according to error analysis.

### Actual result

TODO

### Other notes

TODO Relation level: will relation-level candidate generation help with only a "general-purpose" KB (e.g. Freebase)? How?


## Domain-specific KB

Hypothesis: using a general-purpose KB to generate candidates will cover most errors OCR make.

TODO (most are the same with above)

### Protocol

- KB to use:
  - PaleoDB dump

- Implementation: same as above


### Proxy: how to evaluate hypothesis

Similar to above, calculate recall on evaluation document set, and compare it to other :
- system recall without candidate generation (dd)
- optimal recall of selecting from one OCR output (opt_0)
- optimal recall of selecting from all generated candidates (opt_candgen)
  - To get the system well calibrated, "dd" should approach "opt_candgen".
- optimal recall of selecting from all possible candidates within edit distance X (opt_X)
  - If there's a gap to its according line in opt_X, it shows that we need a better KB. 