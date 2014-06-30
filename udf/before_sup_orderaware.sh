psql -c """drop table if exists orderaware_supv_label cascade;
""" $DB_NAME

psql -c """create table orderaware_supv_label(
  docid TEXT,
  candidate_id TEXT,
  label BOOLEAN
  );
""" $DB_NAME
