#!/usr/bin/python
#By Steve Hanov, 2011. Released to the public domain
import time
import sys


# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words.
class _TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        global NodeCount
        NodeCount += 1

    def insert( self, word ):
        node = self
        for letter in word:
            if letter not in node.children: 
                node.children[letter] = _TrieNode()

            node = node.children[letter]

        node.word = word

# Global objects
NodeCount = 0
WordCount = 0
trie = _TrieNode()

def init(DICTIONARY):

    # read dictionary file into a trie
    # trie = _TrieNode()
    global trie, NodeCount, WordCount

    # for word in open(DICTIONARY, "rt").read().split():
    for word in [l.strip() for l in open(DICTIONARY).readlines()]:
        WordCount += 1
        trie.insert( word )
    print >>sys.stderr, "Read %d words into %d nodes" % (WordCount, NodeCount)

# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search( word, maxCost ):

    # build first row
    currentRow = range( len(word) + 1 )

    results = []

    # recursively search each branch of the trie
    for letter in trie.children:
        _searchRecursive( trie.children[letter], letter, word, currentRow, 
            results, maxCost )

    return results

# The search function returns a list of all words that are less than the given
# maximum distance from the target word
# if maxCandNum = 0, return all; otherwise return some.
# returns:
#   [(candword, dist)]
def searchTops( word, maxCost, maxCandNum = 0 ):

    # TODO Slow implementation
    results = []
    for i in range(1, maxCost + 1):
        results = search(word, i)
        # Already get enough results
        if maxCandNum == 0: # unristricted
            return sorted(results, key=lambda x:x[1])
        if len(results) >= maxCandNum:
            return sorted(results, key=lambda x:x[1])[:maxCandNum]

    # return last-round result if cannot meet enough candidates
    return sorted(results, key=lambda x:x[1])[:maxCandNum]

# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def _searchRecursive( node, letter, word, previousRow, results, maxCost ):

    columns = len( word ) + 1
    currentRow = [ previousRow[0] + 1 ]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in xrange( 1, columns ):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[ column - 1 ] + 1
        else:                
            replaceCost = previousRow[ column - 1 ]

        currentRow.append( min( insertCost, deleteCost, replaceCost ) )

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.word != None:
        results.append( (node.word, currentRow[-1] ) )

    # if any entries in the row are less than the maximum cost, then 
    # recursively search each branch of the trie
    if min( currentRow ) <= maxCost:
        for letter in node.children:
            _searchRecursive( node.children[letter], letter, word, currentRow, 
                results, maxCost )

## MAIN func
if __name__ == '__main__':
    tottime = 0.0
    DICTIONARY = sys.argv[1]
    MAX_COST = int(sys.argv[2])
    NUMWORDS = int(sys.argv[3])
    init(DICTIONARY)

    # Test
    for word in [l.strip() for l in open("/usr/share/dict/words").readlines()[:NUMWORDS]]:
        start = time.time()
        # results = search( TARGET, MAX_COST )
        results = search( word, MAX_COST )
        end = time.time()
        print '%s: %d candidates.' % (word, len(results))
        print ' ', sorted(results, key=lambda x:x[1])[:10]
        # for result in results: 
            # print result
        print "Search took %g s" % (end - start)

        tottime += (end - start)

    print 'Total time:', tottime, '#Words:', NUMWORDS, 'Avg speed:', tottime / float(NUMWORDS)
