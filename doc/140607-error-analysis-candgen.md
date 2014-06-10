# First round of candidate generation

Supervised by 3gram

ddocr_100_textid=# SELECT source, label, count(*) FROM candidate
ddocr_100_textid-#   GROUP BY source, label
ddocr_100_textid-#   ORDER BY source, label;
 source | label | count  
--------+-------+--------
 C      | f     | 202946
 C      | t     |  30398
 C      |       | 230529
 CSg    | f     |  24121
 CSg    | t     |   1109
 CSg    |       |  54380
 CT     | f     |     20
 CT     | t     | 386412
 CT     |       | 120793
 CTSg   | f     |   2192
 CTSg   | t     |     20
 CTSg   |       |   1601
 T      | f     |  13344
 T      | t     | 190972
 T      |       | 193143
 TSg    | f     |   2995
 TSg    | t     |    858
 TSg    |       |   8774
(18 rows)

00:10:05 [sampler] INFO  # nvar               : 1464607
00:10:05 [sampler] INFO  # nfac               : 15961389
00:10:05 [sampler] INFO  # nweight            : 203
00:10:05 [sampler] INFO  # nedge              : 17025753


 source | label | count5 | count3
--------+-------+--------+--------
 C      | f     | 163115 | 202946
 C      | t     |  20481 |  30398
 C      |       | 280277 | 230529
 CSg    | f     |  19584 |  24121
 CSg    | t     |    782 |   1109
 CSg    |       |  59244 |  54380
 CT     | f     |     16 |     20
 CT     | t     | 342711 | 386412
 CT     |       | 164498 | 120793
 CTSg   | f     |   1843 |   2192
 CTSg   | t     |     16 |     20
 CTSg   |       |   1954 |   1601
 T      | f     |  10783 |  13344
 T      | t     | 151798 | 190972
 T      |       | 234878 | 193143
 TSg    | f     |   2443 |   2995
 TSg    | t     |    376 |    858
 TSg    |       |   9808 |   8774
(18 rows)


A case that generated is correct:

 JOURNAL_26741@6122_0.0 | JOURNAL_26741@6122_0 | JOURNAL_26741 |  6122 |      0 | C      |      0 | coefflcients     |   12 |  489 | 1384 |  680 | 1413 |     |        |
 JOURNAL_26741@6122_1.0 | JOURNAL_26741@6122_1 | JOURNAL_26741 |  6122 |      1 | T      |      0 | coeﬂicients      |   12 |  488 | 1382 |  680 | 1413 | NNS | O      | coeﬂicients
 JOURNAL_26741@6122_2.0 | JOURNAL_26741@6122_2 | JOURNAL_26741 |  6122 |      2 | CSg    |      0 | coefficients     |      |      |      |      |      |     |        |
 JOURNAL_26741@6122_3.0 | JOURNAL_26741@6122_3 | JOURNAL_26741 |  6122 |      3 | TSg    |      0 | coeﬁicients      |      |      |      |      |      |     |        |



# Back to non-cand-gen

results even worse with supv3

 source | label | OrdAw  
--------+-------+--------
 C      | f     | 212785
 C      | t     |  48354
 C      |       | 202734
 CT     | t     | 388875
 CT     |       | 118350
 T      | f     |  16515
 T      | t     | 228425
 T      |       | 152519