# Clean up cand_word
echo "Updating cand_word and candidate..."
psql -c "
  INSERT INTO cand_word(cand_word_id, candidate_id, docid, varid, candid, source, wordid, word)
  SELECT cand_word_id, candidate_id, docid, varid, candid, source, wordid, word 
  FROM generated_cand_word;
" $DB_NAME

psql -c "ANALYZE cand_word;" $DB_NAME

psql -c "INSERT INTO candidate (
               variable_id, candidate_id, docid, varid, candid, source) 
        SELECT (docid || '@' || varid) as variable_id,
                candidate_id, docid, varid, candid, source
        FROM    generated_cand_word
        GROUP BY docid, candidate_id, varid, candid, source
        
        ;
" $DB_NAME

psql -c "ANALYZE candidate;" $DB_NAME
