#! /usr/bin/env bash
psql -c "TRUNCATE labels_disg CASCADE;" $DB_NAME
