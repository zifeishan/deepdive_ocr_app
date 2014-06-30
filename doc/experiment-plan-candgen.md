Similarity / Distance Measure
====

This section discusses possible similarity / distance measures used for generating new candidates. Suppose we have a measure `dist`, here's a way to generate candidates:

Given a word or a sequence of words `s`, find another string `s'` in KB, s.t., `dist(s, s') < threshold`.

Another possible way is: generating the top-K candidates that has smallest distance or highest similarity.

In the following, we discuss some possible distance measures to use.

## Edit distance

- Our last experiment justifies edit distance measure. According to Figure 1:
  - About 30--50% errors are within edit distance 1. 
    - This means that, if all possible candidates within edit distance 1 to OCR outputs are generated, we can reduce 30--50% errors from an "optimal" system that selects the correct answer from OCRs.
  - About 50--70% errors are within edit distance 3.

(Figure)

TODO give exact numbers for error reduction rate for opt(X), X=1..5

## OCR-Specific Edit Distance

Each OCR system makes independent errors. For example, some recognizes "rm" as "nn", "e" to "c", or "fi" to a single character. These are all "edits" but different edit operations. We may consider treating different kinds of edits differently, and learn weights for them accordingly.

We may use this in finding new candidates, which has a high cost; we may also use it only as a feature for generated candidates, which has a lower cost.

## Other possible measures

- Trigram similarity / distance
  - For string x and y, TX / TY is the bag of trigrams of x / y, sim(x, y) is the Jaccard similarity of TX and TY; dist(x, y) is the Jaccard distance of TX and TY.

## References

### Trigrams

http://wiki.postgresql.org/wiki/What%27s_new_in_PostgreSQL_9.1#K-Nearest-Neighbor_Indexing

http://postgresql.1045698.n5.nabble.com/Index-for-Levenshtein-distance-td5764546.html

http://dba.stackexchange.com/questions/59653/postgres-levenshtein-distance-and-nested-queries

http://stackoverflow.com/questions/12100983/using-levenshtein-function-on-each-element-in-a-tsvector

### Levenshtein (with Trie)

http://stackoverflow.com/questions/4868969/implementing-a-simple-trie-for-efficient-levenshtein-distance-calculation-java

http://murilo.wordpress.com/2011/02/01/fast-and-easy-levenshtein-distance-using-a-trie-in-c/

http://stevehanov.ca/blog/index.php?id=114

http://en.wikipedia.org/wiki/BK-tree

TODO other measures?

----

Candidate generation Experiments
====

This section discusses the next-step experiments we want to conduct for candidate generation. It includes using a general-purpose KB, a domain-specific KB, and in the future, using relation-level KBs.

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
- system recall without candidate generation (dd_kb_general)
- optimal recall of selecting from one OCR output (opt_0)
- optimal recall of selecting from all generated candidates (opt_candgen_general)
  - To get the system well calibrated, "dd_kb_general" should approach "opt_candgen_general".
- optimal recall of selecting from all possible candidates within edit distance X (opt_X)
  - If there's a gap to its according line in opt_X, it shows that we need a better KB. 

### Expected result

Generating candidates within edit distance X using a general-purpose KB, Line "dd_kb_general" should go above opt_0 (at least slightly), but it can never go higher than opt_X.

We expect that there is a large gap between dd and opt_X. To fill this gap, we need to do error analysis. Hopefully most errors can be covered by using a domain-specific KB.

### Next step

If error analysis shows that domain-specific KB helps, we will implement candidate generation with domain-specific KB.

Otherwise we will fix errors according to error analysis.

### Actual result

TODO

### Other notes

TODO Relation level: will relation-level candidate generation help with only a "general-purpose" KB (e.g. Freebase)? How?

----

## Domain-specific KB (entity-level)

Hypothesis: in addition to a general-purpose KB, using a domain-specific KB to generate candidates using an entity-level method, will cover most errors OCR make.

### Protocol

- KB to use:
  - PaleoDB dump

- Implementation: same as above


### Proxy: how to evaluate hypothesis

Similar to above, calculate recall on evaluation document set (dd_kb_domain), and compare it to dd_kb_general / opt_0 / opt_candgen_domain / opt_X.

- If there's a gap to its according line in opt_X, it shows that we still need a better KB. 


### Expected result

We expect that domain-specific KB outperforms the general-purpose one by a large margin. 

Specifically, generating candidates within edit distance X using a domain-specific KB, line "dd" should go above opt_0 by a large margin, and approach opt_X.

### Next step

The next step is some error analysis. If remaining errors can be coverd by a relation-level KB, we will consider implementing it.

We might also benefit from **OCR-specific candidate generation strategies**, e.g. OCR-specific edit distance.

If error analysis shows that domain-specific KB helps, we will implement candidate generation with domain-specific KB.

Otherwise we will fix errors according to error analysis.

### Actual result

TODO

----

## Domain-specific KB (relation-level)

Hypothesis: Adding relation-level candidate generation methods to a domain-specific KB will lead to a boost to error reduction.

TODO
