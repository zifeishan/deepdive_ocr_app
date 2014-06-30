I feel like that we are not systematic enough here--we used to be much
more systematic when we explored the space w/o candidate generation
(that is how we discover that the order-aware distant supervision
works!), we need to have the same, if not higher, bar here for
candidate generation. My suggestion is to use the Assembla wiki more,
and document the approach that  you want to try before you actually
implement it. For each approach:

    1. (hypothesis) Why do you choose this approach to implement? (What hypothesis do you want to accept/reject?)
    2. (protocol) What is the precise protocol of the implementation?
    3. (proxy) How to measure whether your hypothesis is correct?
    4. (expected result) What is your expected result?
    5. (next step) What is the next approach to implement?
    6. (actual result) What is the actual result?

Writing down items 1-5 for each approach that you planned to try is
far more important than getting 6 without 1-5, no matter how good the
actual result is.

Writing down 1-5 requires error analysis, which is missing. 

Note that 5 does *not* rely on 6--you need to plan the next several
steps before you implement anything.

Can you write some notes with this template on the Wiki? We can
iterate to improve it. I can also Skype whenever you want to elaborate
what I mean.

>> Specifically I am now trying to build some trigram index to speed it up, according to Ce's advice.

We need to be systematic here. Just to make sure that Chris is also on
the same page, the query that Zifei wants to answer is:

      Given a string s, find another string s' \in KB, s.t., sim(s, s') < threshold.

   1. First, what is sim(-.-)? Seems that you are assuming that sim(-,-) is edit distance. Why? (I am not convinced here--where is the error analysis to justify this choice?)
   2. After we have justified the choice of sim(-,-), we need to consider how to evaluate this query:
       2.1 Can PostgreSQL/Greenplum deal with this query efficiently? 
       2.2 If 2.1 fails, find some papers about fuzzy string matching, and pick their approach--We do not want to invent anything here.
       2.3 If 2.2 fails, which is highly unlikely, we need to discuss it much more deeply.

It seems that step 1 is still missing. To answer this question, we
need error analysis. Before we do error  analysis, we need a taxonomy
of a simple survey of popular similarities that people are using.

>> for words that are not in English dictionary, generate a candidate that is the most similar word that appear frequently (>=3 times) in current document
>> This process yields some correct candidates but also lots of incorrect ones. For evaluation, the result is not better but slightly worse than that without candidate generation (the system is trained with all previous features as well as an edit-distant feature).

This heuristic worries me. Why do we try this rule? Why do you think
this rule is a "naive candidate  generation strategy"? Where is the
constant 3 comes from? What do you mean by "similar"? Why generate "a
candidate" not two or more? Why only generate candidate for words that
are not in English  dictionary?

We need error analysis to justify *why do we choose this rule*.


Ce