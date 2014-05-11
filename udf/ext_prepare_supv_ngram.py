import ddext

def init():
  ddext.input('docid', 'text')
  ddext.input('words', 'text[]')
  ddext.input('gram_len', 'bigint')
  ddext.returns('docid', 'text')
  ddext.returns('ngram', 'text')

def run(docid, words, gram_len):
  for i in range(0, len(words) - gram_len + 1):
    yield docid, ' '.join(words[i : i + gram_len])
