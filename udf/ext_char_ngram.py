#! /usr/bin/env python

import ddext

def init():
  ddext.input('docid', 'TEXT')
  ddext.input('candidate_id', 'TEXT')
  ddext.input('word', 'text')
  ddext.input('gram_len', 'int')

  ddext.returns('docid', 'TEXT')
  ddext.returns('candidate_id', 'TEXT')
  ddext.returns('ngram', 'text')
  ddext.returns('count', 'int')

def run(docid, candidate_id, word, gram_len):
  def IsASCII(s):
    return all(ord(c) < 128 for c in s)

  if 'encoding' in SD:
    encoding = SD['encoding']
  else:
    import unicodedata
    rv = plpy.execute("select setting from pg_settings where name = 'server_encoding'");
    encoding = rv[0]["setting"]
    SD['encoding'] = encoding     # should be "UTF8"
    # plpy.info(encoding)

  ascword = word.decode(encoding)
  ngram = {}
  for i in range(len(ascword) - gram_len):
    s = ascword[i : i + gram_len]
    # if not IsASCII(s):
    #   plpy.info(s)   # This would fail, since "info" tries to str() it
    if not IsASCII(s):  # Only extract non-ASCII chars...
      if s not in ngram:
        ngram[s] = 0
      ngram[s] += 1

  return [(docid, candidate_id, gram, ngram[gram]) for gram in ngram]
