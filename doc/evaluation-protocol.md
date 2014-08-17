Evaluation Protocol
====

## Dataset

We are given training dataset `LabeledDoc(docid, wordid, word)`, which is extracted from hand-labeled documents (HTML files) that we assume correct. For evaluation, we hold out a fraction of supervision set `LabeledDoc` as `Test`, and calculate the recall of predicted words on the testing set. We always hold out **entire documents**, e.g. all rows with $docid = 1, 4, 7$ in `LabeledDoc`. 

To generate `Test(docid, wordid, word)`, we also clean up the original dataset, to extract only what we care for evaluation. Specifically, we remove:

- Non-English paragraphs
- Figures and tables
- References
- Contents from HTML that does not match original paper.

## Method

The high-level idea is following: any OCR output for a document can be viewed as a sequence of words. We try to find the optimal match between this word sequence and the ground-truth word sequence in evaluation dataset.

We also try to measure the best possible output of a "candidate lattice" that include all candidates given by different OCRs and our generated candidates. We use Dynamic Programming to find the optimal possible world, where selected candidates has the optimal match to evaluation dataset.

## Evaluating a word sequence

For any sequence of word denoted as `Predicted`, we select `Predicted` relation for each `docid` in the holdout dataset `Test`: 

$$ Predicted = Doc \Join \pi_{docid}(Test) $$

The naive evaluation assuming perfect alignment is:

$$ Recall = \frac{|Predicted \Join Test|}{|Test|} $$

However the naive evaluation would wrongly punish misalignments. To fix it, we enable any shifting of words while preserving orders, that can maximize the number of matched words in the testing set.

**Evaluation for each single document:** 
For each $docid = did$ in Test, denote: 
$$Test_{did} = \sigma_{docid=did}(Test)$$
$$Predicted_{did} = \sigma_{docid=did}(Predicted)$$ 


Calculate the optimal mapping for document `did`, denoted as $Map_{did}$, which generates the relation MappedPred that has the maximal number of matched words with $Test_{did}$:


<!-- $$ s.t. Map_{did}(i) = j \iff MappedPred(docid, i) = Pred(j) $$ -->


$$
\begin{aligned}
Map_{did} = \mbox{ }
      & argmax_{Map_{did}}(|MappedPred \Join Test_{did}|) \\
      &  \mbox{s.t.  } Map_{did}(i) = j \iff
                \pi_{word} \sigma_{wordid = i} MappedPred = \pi_{word} \sigma_{wordid = j} Pred_{did} \\
      & \mbox{and  }
                i < j \rightarrow Map_{did}(i) < Map_{did}(j), \forall i, j \in \pi_{wordid} MappedPred 
\end{aligned}
$$

<!-- 
% \left\{
%         \begin{array}{ll}
%                 True  & \mbox{if } c_i \in 1gram \\
%                 False & \mbox{if } c_i \not\in 1gram \vee \exists c_j, \mbox{s.t. } f(v, c_j)=True
%         \end{array}
% \right.



$$ Map_{did} = argmax_{Map_{did}}(|MappedPred \Join Test_{did}|) $$
$$ s.t.  Map_{did}(i) = j \iff
\pi_{word} \sigma_{wordid = i} MappedPred
= \pi_{word} \sigma_{wordid = j} Pred_{did} $$
$$ \bigwedge
i < j \rightarrow Map_{did}(i) < Map_{did}(j), \forall i, j \in \pi_{wordid} MappedPred $$

 -->


The optimal mapping can be calculated by dynamic programming, with a time complexity of $O(n^2)$.

We can therefore define the Precision and Recall:
$$Precision_{did} = \frac { |Map_{did}| }{ |Predicted_{did}|} $$
$$Recall_{did} = \frac { |Map_{did}| }{ |Test_{did}|} $$

Since our evaluation dataset is reduced, many words from `Predict` is not present in `Test`. Therefore a reasonable way for evaluation is not to punish deletions from `Predict` to `Test`, thus we only choose **Recall** as our evaluation metric.

<!-- And we can use the F1 score for evaluating the overall performance:

$$F1_{did} = \frac{2Precision_{did}Recall_{did}}{Precision_{did} + Recall_{did}}$$
 -->