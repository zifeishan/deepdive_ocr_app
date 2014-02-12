#! /usr/bin/env bash
psql -c "TRUNCATE filtered_labels CASCADE;" ddocr
