Results in: experiments/2014-07-21T091925-candgen-d2-segcomb/

09:37:25 [profiler] INFO  --------------------------------------------------
09:37:25 [profiler] INFO  Summary Report
09:37:25 [profiler] INFO  --------------------------------------------------
09:37:25 [profiler] INFO  ext_naivefeature SUCCESS [151333 ms]
09:37:25 [profiler] INFO  ext_cand_2gram SUCCESS [424314 ms]
09:37:25 [profiler] INFO  ext_char_1gram SUCCESS [441070 ms]
09:37:25 [profiler] INFO  ext_cand_2gram_feature SUCCESS [41231 ms]
09:37:25 [profiler] INFO  ext_sup_use_orderaware SUCCESS [494869 ms]
09:37:25 [profiler] INFO  inference_grounding SUCCESS [96026 ms]
09:37:25 [profiler] INFO  inference SUCCESS [475627 ms]
09:37:25 [profiler] INFO  calibration plot written to /lfs/madmax2/0/zifei/deepdive/out/2014-07-21T091925/calibration/candidate.label.png [0 ms]
09:37:25 [profiler] INFO  calibration SUCCESS [10935 ms]


# JOURNAL_58670 (candgen does not improve quality)

X why not picked in opt?
    sparse
    fragmentary

    # Not sure why it is problematic. ".matches.0 sometimes has error?"

      X       sparse
      .       .
      .       What
      .       is
      .       preserved
      .       is
      .       often
      X       fragmentary  --> should be '.'
      .       ,
      .       making


6 Chatelperronian -> Châtelperronian
  ’s -> 's (should be solved already)
  VIII-X
  modem -> modern *solution: direct / generate candidates even if already correct*
  6/mid- = * 11'Igonicl -> 6/mid-trigonid *(cannot fix)*
  n 14 -> n = 14

Maybe cpp will have a better score than py, since our python impl assumes that vars must have consequent words??

(up to 7%)