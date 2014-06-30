psql -c """drop table if exists generated_cand_word cascade;
""" $DBNAME

psql -c """create table generated_cand_word(
    docid         TEXT,
    cand_word_id  TEXT,
    candidate_id  TEXT,
    varid         INT,      -- start from 1
    candid        INT,      -- start from 0, according to source
    source        TEXT,     -- 1-1 mapping to source
    wordid        INT,      -- start from 0
    word          TEXT,
    distance      INT       -- edit distance from original word
    )
-- DISTRIBUTED BY (docid);
""" $DBNAME  # TODO???


# Clean up cand_word
echo "Clean up cand_word..."
psql -c """
  DELETE FROM cand_word
  WHERE source like '%Sg';

  DELETE FROM candidate
  WHERE source like '%Sg';

  ANALYZE cand_word;
  ANALYZE candidate;
""" $DBNAME
