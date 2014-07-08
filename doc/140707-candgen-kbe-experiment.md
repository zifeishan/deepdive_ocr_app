Using KB:

Edit distance 1 hardly improves results...
100x

ddocr_100_candgen=# select source, label, count(*) from candidate group by source,label order by source,label
ddocr_100_candgen-# ;
 source | label | count
--------+-------+--------
 C      | f     | 223447
 C      | t     |  47175
 C      |       | 193251
 CSg    | f     | 494083
 CSg    | t     |  10209
 CSg    |       | 767179
 CT     | f     |    256
 CT     | t     | 383416
 CT     |       | 123553
 CTSg   | f     | 374022
 CTSg   | t     |    506
 CTSg   |       | 232365
 T      | f     |  22142
 T      | t     | 228467
 T      |       | 146850
 TSg    | f     |  96388
 TSg    | t     |    525
 TSg    |       | 392870
(18 rows)


Edit distance 2
10,000x


Edit distance 3 is too much: (1,000,000x)

22:32:13 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_67391] Generated 608387 cands (611148 words) : original 16010 words
22:32:13 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_57941
22:33:00 [taskManager] INFO  Memory usage: 235/1962MB (max: 27159MB)
22:33:01 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_533] Generated 1567603 cands (1579440 words) : original 30748 words
22:33:01 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_18997
22:33:38 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_63084] Generated 1310746 cands (1321509 words) : original 32691 words
22:33:38 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_67169
22:34:00 [taskManager] INFO  Memory usage: 235/1962MB (max: 27159MB)
22:34:22 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_18100] Generated 774241 cands (781560 words) : original 25907 words
22:34:22 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_57898
22:34:50 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_40306] Generated 905281 cands (909024 words) : original 20994 words
22:34:50 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_27760
22:34:59 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_57782] Generated 515676 cands (517298 words) : original 10324 words
22:34:59 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_27901
22:35:00 [taskManager] INFO  Memory usage: 235/1962MB (max: 27159MB)
22:35:34 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_35998] Generated 677105 cands (680682 words) : original 20599 words
22:35:34 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_45757
22:35:37 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_67590] Generated 769112 cands (776110 words) : original 19449 words
22:35:37 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_17920
22:36:00 [taskManager] INFO  Memory usage: 235/1962MB (max: 27159MB)
22:36:14 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_18997] Generated 794333 cands (797124 words) : original 10155 words
22:36:14 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_5142
22:36:34 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_45405] Generated 1111508 cands (1116971 words) : original 16761 words
22:36:56 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_57941] Generated 884079 cands (888189 words) : original 19414 words
22:36:56 [extractorRunner-ext_cand_gen_kbe] INFO  Processing JOURNAL_54374
22:37:00 [taskManager] INFO  Memory usage: 235/1962MB (max: 27159MB)
22:37:03 [extractorRunner-ext_cand_gen_kbe] INFO  [JOURNAL_45757] Generated 341361 cands (341831 words) : original 4579 words

Look at results:

JOURNAL_13504   JOURNAL_13504@1_54.0    JOURNAL_13504@1_54      1       54      CTSg    0       Ems     3
JOURNAL_13504   JOURNAL_13504@1_64.0    JOURNAL_13504@1_64      1       64      CTSg    0       Ixa     3
JOURNAL_13504   JOURNAL_13504@1_3.0     JOURNAL_13504@1_3       1       3       CTSg    0       Cava    3
JOURNAL_13504   JOURNAL_13504@1_98.0    JOURNAL_13504@1_98      1       98      CTSg    0       NP9     3
JOURNAL_13504   JOURNAL_13504@1_99.0    JOURNAL_13504@1_99      1       99      CTSg    0       NP8     3
JOURNAL_13504   JOURNAL_13504@1_121.0   JOURNAL_13504@1_121     1       121     CTSg    0       Zia     3
JOURNAL_13504   JOURNAL_13504@1_94.0    JOURNAL_13504@1_94      1       94      CTSg    0       NP5     3
JOURNAL_13504   JOURNAL_13504@1_95.0    JOURNAL_13504@1_95      1       95      CTSg    0       NP4     3
JOURNAL_13504   JOURNAL_13504@1_96.0    JOURNAL_13504@1_96      1       96      CTSg    0       NP7     3
JOURNAL_13504   JOURNAL_13504@1_97.0    JOURNAL_13504@1_97      1       97      CTSg    0       NP6     3