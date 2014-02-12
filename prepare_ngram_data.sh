#! /bin/bash

# Configuration
DB_NAME=ddocr
DB_PORT=5437
cd `dirname $0`
BASE_DIR=$1
# dropdb $DB_NAME
# createdb $DB_NAME

# psql -p $DB_PORT -c "drop schema if exists public cascade; create schema public;" $DB_NAME
psql -p $DB_PORT -c "create table ngram_1(
  id BIGSERIAL PRIMARY KEY, 
  gram TEXT, 
  count INT);" $DB_NAME

# psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/$1'" $DB_NAME  # escaped \t

psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/0.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/4.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/8.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/c.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/g.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/k.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/o.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/s.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/w.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/1.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/5.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/9.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/d.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/h.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/l.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/other.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/punctuation.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/t.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/x.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/2.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/6.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/a.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/e.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/i.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/m.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/p.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/q.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/u.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/y.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/3.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/7.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/b.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/f.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/j.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/n.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/pos.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/r.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/v.ngram'" $DB_NAME 
psql -p $DB_PORT -c "COPY ngram_1(gram, count) FROM '$BASE_DIR/z.ngram'" $DB_NAME 
