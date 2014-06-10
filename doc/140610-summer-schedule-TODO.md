Summer Schedule
====

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
