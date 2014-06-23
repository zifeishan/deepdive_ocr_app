# Clean up cand_word
echo "Updating cand_word and candidate..."
psql -c "
  INSERT INTO cand_word(docid, cand_word_id, candidate_id, varid, candid, source, wordid, word)
  SELECT docid, cand_word_id, candidate_id, varid, candid, source, wordid, word 
  FROM generated_cand_word;
" $DBNAME

psql -c "ANALYZE cand_word;" $DBNAME

psql -c "INSERT INTO candidate (
               docid, variable_id, candidate_id, varid, candid, source) 
        SELECT  docid,
                (docid || '@' || varid) as variable_id,
                candidate_id,  varid, candid, source
        FROM    generated_cand_word
        GROUP BY docid, candidate_id, varid, candid, source
        
        ;
" $DBNAME

psql -c "ANALYZE candidate;" $DBNAME
