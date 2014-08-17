# $1: CandGen source

# Clean up cand_word
echo "Updating cand_word and candidate..."
psql -c "
  INSERT INTO cand_word(docid, cand_word_id, candidate_id, varid, candid, source, wordid, word)
  SELECT docid, cand_word_id, candidate_id, varid, candid, source, wordid, word 
  FROM generated_cand_word_$1;
" $DBNAME

psql -c "ANALYZE cand_word;" $DBNAME

psql -c "INSERT INTO candidate (
               docid, variable_id, candidate_id, varid, candid, source) 
        SELECT  docid,
                (docid || '@' || varid) as variable_id,
                candidate_id,  varid, candid, source
        FROM    generated_cand_word_$1
        GROUP BY docid, candidate_id, varid, candid, source
        
        ;
" $DBNAME

psql -c "ANALYZE candidate;" $DBNAME

# # Generate an aggregated "candidate" table
# psql -c "DROP TABLE IF EXISTS generated_candidates CASCADE;" $DBNAME

# psql -c "
# CREATE TABLE generated_candidates AS
# SELECT  docid, 
#         candidate_id, 
#         max(source)   as source, 
#         max(distance) as distance, 
#         -- max(original_word) as original_word,
#         max(varid)    as varid,
#         max(candid)   as candid
#         -- , array_agg(word order by wordid) as words
# FROM generated_cand_word_$1
# GROUP BY docid, candidate_id;" $DBNAME

# psql -c "
# CREATE TABLE generated_candidates AS
# SELECT  docid, 
#         candidate_id, 
#         source, 
#         distance, 
#         original_word,
#         varid,
#         candid,
#         array_agg(word order by wordid) as words
# FROM generated_cand_word_$1
# GROUP BY docid, candidate_id, source, distance, original_word, varid, candid
# ;" $DBNAME