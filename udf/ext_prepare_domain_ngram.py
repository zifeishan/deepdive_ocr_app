import ddext

def init():
  ddext.input('docid', 'text')
  ddext.input('words', 'text[]')
  ddext.input('gram_len', 'bigint')
  ddext.input('count_filter', 'bigint')
  ddext.returns('docid', 'bigint')
  ddext.returns('ngram', 'text')
  ddext.returns('count', 'real')

def run(docid, words, gram_len, count_filter):
  ngrams = {}
  for i in range(0, len(words) - gram_len + 1):
    gram = ' '.join(words[i : i + gram_len])
    if gram not in ngrams:
      ngrams[gram] = 1
    else:
      ngrams[gram] += 1
  for gram in ngrams:
    if ngrams[gram] >= count_filter:
      yield docid, gram, ngrams[gram]