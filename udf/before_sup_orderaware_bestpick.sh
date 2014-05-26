psql -c """drop table if exists $1 cascade;
""" $DB_NAME

psql -c """create table $1 (
  id BIGSERIAL PRIMARY KEY,
  docid TEXT,
  candidate_id TEXT,
  label BOOLEAN
  );
""" $DB_NAME
