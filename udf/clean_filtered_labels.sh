#! /usr/bin/env bash
psql -c "TRUNCATE filtered_labels CASCADE;" ddocr
psql -c "DROP TABLE IF EXISTS filtered_labels CASCADE;" ddocr
