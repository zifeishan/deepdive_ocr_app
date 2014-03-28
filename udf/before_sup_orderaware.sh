psql -c """drop table if exists orderaware_supv_label cascade;
""" $DB_NAME

psql -c """create table orderaware_supv_label(id BIGSERIAL PRIMARY KEY, 
  docid TEXT,
  candidate_id BIGSERIAL,
  label BOOLEAN
  );
""" $DB_NAME
