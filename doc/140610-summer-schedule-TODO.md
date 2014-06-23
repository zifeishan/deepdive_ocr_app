Summer Schedule
====

## Updated

1. Generate optimal candidate generation plot
  - within edit distance 0, 1, 2...
  - candidate generation "supervised" by ground truth!

2. Feature engineering (approach the optimal line):
  - implement all candidate generation methods:
    - domain-independent 
    - entity KB
    - relation KB

3. Large datasets (>1K)
  - future: arXiv? (new, 900,000 papers, see Denny's folder)
  - SD
  - 


## Data model for candidate generation

Allow variable "merging"

find "cuts" among variables

--------


- Debug order aware supervision with candidate generation (Jun 11)
  - Optional: minimizing edit distance rather than maximizing #matches in supervision?

- Implement new candidate generation methods:
  1. Implement candidate generation with Entity KB (Jun 11)
  2. generate by splits / combines / ... (Jun 11)
  3. generate a candidate that appears in "domain corpus" by edit distance (optional)
  4. (domain-specific) Relation KB (optional)

- Potential features to add
  - NLP extraction
  - POS/NER N-gram
  - dependency path
  - 

- Refine Evaluation
  - Filter invalid HTML supervision documents
  - Generate macro/micro averages
    - Evaluate by edit distance? (maybe does not make sense since it is a superset...)
    - TODO evaluate by SCLITE?
  
- Design & run experiments on whole Paleo
  - Candidate generation edit distance filter
  - N-gram supervision (N) (?)
  - 

Dataset: prepare for other datasets
  Getting PLoS dataset
  (Why does the crawler get stuck every ~800 documents?)
  Already got 17K papers from SD; watch and wait for the rest 20K.
  PharmGKB, GoogleBook
  Crowdsource manual labels for old documents (to justify our capability)
