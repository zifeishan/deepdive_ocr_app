psql -c """drop table if exists orderaware_supv_label cascade;
""" $DB_NAME

# TODO cannot get rid of ID as long as using old extractor
psql -c """create table orderaware_supv_label(
  id BIGSERIAL PRIMARY KEY,
  docid TEXT,
  candidate_id BIGINT,
  label BOOLEAN
  );
""" $DB_NAME
