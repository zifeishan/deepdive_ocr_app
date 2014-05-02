psql -c """drop table if exists $1 cascade;
""" $DB_NAME

psql -c """create table $1 (
  id BIGSERIAL PRIMARY KEY,
  docid TEXT,
  candidate_id BIGINT,
  label BOOLEAN
  );
""" $DB_NAME
