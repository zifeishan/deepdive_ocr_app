//
//  ext_sup_orderaware.cpp
//  Zifei Shan
//

// INPUT:
//    '''
//    SELECT  docid,
//    array_to_string(array_agg(candidate_id order by varid, candid, wordid), ',' ) AS arr_candidate_id,
//    array_to_string(array_agg(varid order by varid, candid, wordid), ',' ) AS arr_varid,
//    array_to_string(array_agg(wordid order by varid, candid, wordid), ',' ) AS arr_wordid,
//    array_to_string(array_agg(word order by varid, candid, wordid), '~~~^^^~~~' ) AS arr_word
//    FROM    cand_word
//    GROUP BY docid
//    '''

#include <iostream>
#include <fstream>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <set>
#include <vector>
#include <queue>

# define DEBUGCODE(x)
# define SAMPLECODE(x)
# define RELEASECODE(x) x
extern FILE *stderr;

using namespace std;

# define MAXLEN 100000
# define MAXVARS 100000
# define MAXCANDS 100
/**
 * Split a string with delimiter
 */
vector< string > split(string s, string delim)
{
    int last = 0;
    vector<string> ret;
    for(int i = 0; i + delim.size() <= s.size(); i++)
    {
        bool ok = true;
        for(int j = 0; j < delim.size() && ok; j++)
            ok = s[i + j] == delim[j];
        if(ok)
        {
            if(i - last) ret.push_back(s.substr(last, i - last));
            last = i + delim.size();
        }
    }
    if(last < s.size()) ret.push_back(s.substr(last));
    return ret;
}

/**
 * Split a string with delimiter
 */
vector< int > split2int(string s, string delim)
{
    int last = 0;
    vector<int> ret;
    for(int i = 0; i + delim.size() <= s.size(); i++)
    {
        bool ok = true;
        for(int j = 0; j < delim.size() && ok; j++)
            ok = s[i + j] == delim[j];
        if(ok)
        {
            if(i - last) ret.push_back(atoi(s.substr(last, i - last).c_str()));
            last = i + delim.size();
        }
    }
    if(last < s.size()) ret.push_back(atoi(s.substr(last).c_str()));
    return ret;
}

int **edges;
int *edge_num;

int tot_edge_count = 0;
void AddEdge(int i, int j)
{
    edges[i][edge_num[i]] = j;
    edge_num[i]++;
    
    tot_edge_count ++;
    
}

/**
 * Return a topology order of all nodes
 */
vector<int> orderedLattice(int N)
{
    vector<int> order;
    set<int> visited;
    queue<int> freenodes;
    int* indegree = new int [N];
    for (int i = 0; i < N; i++)
        indegree[i] = 0;

    // count indegree for all nodes
    for (int i = 0; i < N; i++)
    {
        for(int j = 0; j < edge_num[i]; j++)
        {
            int target = edges[i][j];
            indegree[target]++;
        }
    }
    
    for (int i = 0; i < N; i++)
        if (indegree[i] == 0) {
            freenodes.push(i);
            visited.insert(i);
//            printf("Init node: %d\n", i);
        }
    
    
    while (freenodes.size() > 0)
    {
        int node = freenodes.front();
        freenodes.pop();
        order.push_back(node);

        for(int j = 0; j < edge_num[node]; j++)
        {
            int target = edges[node][j];
            indegree[target] --;
            if (indegree[target] == 0)
            {
                visited.insert(target);
                freenodes.push(target);
            }
        }
    }
    return order;
    
}
int Match(vector<string>& words, vector<string>& transcript, set<int>& matched_words, int n1, int n2)
{
//    int n1 = words.size();
//    int n2 = transcript.size();
    
    if (n1 == 0 ||  n2 == 0) return 0;
    
    // Creating score array (f[i][j]: N*N)
    int** f = new int*[n1];
    for(int i = 0; i < n1; ++i)
    {
        f[i] = new int[n2];
        for (int j = 0; j < n2; ++j)
            f[i][j] = 0;
    }
    
    // Creating path array (path[i * n2 + j]: N*N)
    int * pathi = new int [n1 * n2];
    int * pathj = new int [n1 * n2];
    for (int i = 0; i < n1 * n2; i++){
        pathi[i] = -2;
        pathj[i] = -2;
    }

    // count indegree for all nodes
    int* indegree = new int [n1];
    for (int i = 0; i < n1; i++)
        indegree[i] = 0;
    for (int i = 0; i < n1; i++)
    {
        for(int j = 0; j < edge_num[i]; j++)
        {
            int target = edges[i][j];
            indegree[target]++;
        }
    }
    // init paths and scores for all "zero indegree nodes"
    for (int i = 0; i < n1; i++)
        for (int j = 0; j < n2; j++)
        {
            if (words[i] == transcript[j])
            {
                f[i][j] = 1;
                pathi[i * n2 + j] = -1; // -1 stands for "first match"
                pathj[i * n2 + j] = -1;
            }
        }
    
    // Get topological order
    vector<int> order = orderedLattice(n1);

    DEBUGCODE (
    
        printf("ORDER:\n");
        for (int i = 0; i < 20; i++)
            printf("%d ", order[i]);
        printf("\n");
    )
    
    // DP with topological order
    for (int ordersub = 0; ordersub < order.size(); ordersub++)
    {
        // TODO
        if (ordersub % 1000 == 0)
        {
            cerr << ".";
        }
        // i: last node
        int i = order[ordersub];
        for (int j = 0; j < n2; j++) // j: transcript position
        {
            for (int t = 0; t < edge_num[i]; t++)
            {
                int i2 = edges[i][t]; // i2: next node
                if (i2 < n1 && j+1 < n2 and words[i2] == transcript[j+1])
                {
                    if (f[i2][j+1] < f[i][j] + 1)
                    {
                        f[i2][j+1] = f[i][j] + 1;
                        pathi[i2 * n2 + j+1] = i;
                        pathj[i2 * n2 + j+1] = j;
                    }
                    // TODO consider multi paths!
                }
                if (i2 < n1)
                {
                    if (f[i2][j] < f[i][j])
                    {
                        f[i2][j] = f[i][j];
                        pathi[i2 * n2 + j] = i;
                        pathj[i2 * n2 + j] = j;
                    }
                    // TODO consider multi paths!
                }
                if (j + 1 < n2)
                {
                    if (f[i][j+1] < f[i][j])
                    {
                        f[i][j+1] = f[i][j];
                        pathi[i * n2 + j+1] = i;
                        pathj[i * n2 + j+1] = j;
                    }
                    // TODO consider multi paths!
                }
            }
        }
    }
    
    // BFS to return results
    int maxscore = 0;
    int besti = 0;
    for (int i = 0; i < n1; i++)
    {
        // This is an end node && has highest score so far
        if (edge_num[i] == 0 && maxscore < f[i][n2 - 1])
        {
            maxscore = f[i][n2 - 1];
            besti = i;
            // TODO consider multi paths!
        }
    }
    cerr << "Finished DP. MaxScore:" << maxscore << endl;
    
    int nowi = besti;
    int nowj = n2 - 1;

    set<pair<int, int> > visited_pairs;
    while (nowi >= 0 and nowj >= 0)
    {
        // return matched words by modifying reference
        
        visited_pairs.insert(make_pair(nowi, nowj));
        
        int i = pathi[nowi * n2 + nowj];
        int j = pathj[nowi * n2 + nowj];
        
        set<pair<int, int> >::iterator it = visited_pairs.find(make_pair(i, j));
        if (it != visited_pairs.end()) { // visited
            cerr << "ERROR: visited pair:" << i << " " << j << endl;
            break;
        }
        
//        printf("%d %d -> %d %d", nowi, nowj, i, j);
        if (nowi != i && nowj != j) {  // (only match "matched" words)
            matched_words.insert(nowi);
        }

        // TODO consider multi paths!

        nowi = i;
        nowj = j;
    
    }

    delete [] f;
    delete pathi;
    delete pathj;
    
    return maxscore;

}

//string arr1[MAXLEN];
//string arr2[MAXLEN];

int main(int argc, const char * argv[])
{
    
//    vector<string> tmp  = split("Who\tis\tyour", "\t");
//    cout << tmp[0] << tmp[1] << endl;
    
//    for row in sys.stdin:
//        docid, varids, candids, wordids, words = row.rstrip('\n').split('\t')
    string SUPV_DIR = "/Users/Robin/ssh-afs-deepdive/app/ocr/data/test-supv-eval-doc30/supervision/";
    if (argc > 1) {
        SUPV_DIR = argv[1];
    }

    // DEBUG
    SAMPLECODE(
    ifstream ftest;
    ftest.open("/Users/Robin/ssh-afs-deepdive/app/ocr/data-local/copy_query_func_ext_sup_orderaware6724026584894344512.tsv-aaaaaaaaaa", ifstream::in);
      )

    string line;
    while(std::getline(cin, line)) {
//    while(std::getline(ftest, line)) {
        string docid;
        vector<int> varids;
        vector<int> candids;
        vector<int> wordids;
        vector<string> words;
        vector<string> parts = split(line, "\t");
        
//        cerr << parts.size() << " parts." << endl;
        if (parts.size() != 5)
            continue;
        docid = parts[0];
        varids = split2int(parts[1], ",");
        candids = split2int(parts[2], ",");
        wordids = split2int(parts[3], ",");
        words = split(parts[4], "~~~^^^~~~");
        int N = varids.size();
        
        SAMPLECODE(if (N > 1000) N = 1000;)

        DEBUGCODE(
        for(int i=N-10; i<N; i++)
            printf("%d %d %d %s\n", varids[i], candids[i], wordids[i], words[i].c_str());
          )
        DEBUGCODE(cerr << N << words.size() << varids.size() << candids.size() << wordids.size() << endl;)
        if ( (words.size() != varids.size()) ||
                (words.size() != candids.size()) ||
                (words.size() != wordids.size()) || N == 0)
        {
            cerr << docid << " ERROR: lengths does not match! / Empty data!" << endl;
            continue;
        }
        
        // Load supervision sequence
        string transcript_file = SUPV_DIR + "/" + docid + ".seq";
        
//        if not os.path.exists(transcript_file):
//            print >>sys.stderr, 'SUPERVISION DATA NOT EXISTS:', transcript_file
//            continue

        vector<string> transcript;
        ifstream fin;
        fin.open(transcript_file, ifstream::in);
        string word;
        while( std::getline( fin, word ) ) {
            transcript.push_back(word);
//            cout << word << endl;
        }
        fin.close();
        
        
        int n1 = N;
        int n2 = transcript.size();
        
        SAMPLECODE(if (n2 > 1000) n2 = 1000;)

//        printf("%d %d\n", N, transcript.size());
//        for (int i = 0; i < 10; i++) printf("%s ", transcript[i].c_str());
        
        /**
         * 1. Build directed graph
         */
        
        // Compute maximum variable ID & candidate ID
        int maxv = 0;
        for(int i = 0; i < N; i++) {
            if (maxv < varids[i]) maxv = varids[i];
        }
        int maxc = 0;
        for(int i = 0; i < N; i++) {
            if (maxc < candids[i]) maxc = candids[i];
        }
        
//        // Record for each v and c, the maximum wordid
//        int *index_vc_maxwid = new int[MAXVARS * MAXCANDS];
//        for (int i = 0; i < N; i++)
//        {
//            int v = varids[i];
//            int c = candids[i];
//            int w = wordids[i];
//            if (index_vc_maxwid[v * maxc + c] < w)
//                index_vc_maxwid[v * maxc + c] = w;
//        }

        // Init edges
        edge_num = new int [N];
        for (int i = 0; i < N; i++) edge_num[i] = 0;
        
        edges = new int* [N];
        for (int i = 0; i < N; i++)
            edges[i] = new int [maxc];
        
        DEBUGCODE(cerr << docid << " Building graph.." << endl;)
        // Build graph (add all edges)
        for (int i = 0; i < N; i++)
        {
            int v1 = varids[i];
            int c1 = candids[i];
            if (i+1 < N && varids[i+1] == v1 && candids[i+1] == c1) { // not last word
                AddEdge(i, i + 1);
            }
//            
//            int lastwid = index_vc_maxwid[v1 * maxc + c1];
//            if (w1 != lastwid) // not last word, only connect to next word
//            {
//                if (i + 1 < N)
//                    AddEdge(i, i + 1);
//            }
            else
            {
//                for (int j = 0; j < N; j++) // last word
                for (int j = i + 1; j < N; j++) // all next variables should have sub > i!
                {
                    int v2 = varids[j];
                    // prune:
                    if (v2 > v1 + 1)  // variables are ordered
                        break;
                    if (v2 != v1 + 1)
                        continue;
                    int w2 = wordids[j];
                    if (w2 != 0)
                        continue;
                    // Add an edge to all candidates in NEXT VARID.
                    // TODO: consider skipping triangle case!!
                    AddEdge(i, j);
                }
            }
        }
        
//        printf("#edges: %d\n", tot_edge_count);
//        #edges: 25583 vs 27462 (python)
        
//        delete index_vc_maxwid;
        
        cerr << docid << " Running DP.. N1=" << n1 << ", N2=" << n2 << endl;
        /**
         * 2. Return DP result
         */
        set<int> matched_words;
        int score = Match(words, transcript, matched_words, n1, n2);

        cerr << docid << " Finished running DP.  score=" << score << endl;

        
        // Print all outputs
        set<string> matched_cids;
        int num_matched_words = 0; // >= score
        for (set<int>::iterator it = matched_words.begin(); it != matched_words.end(); it++)
        {
            int i = *it;
            char cid[256] = {};
            sprintf(cid, "%s@%d_%d", docid.c_str(), varids[i], candids[i]);

            set<string>::iterator findcid = matched_cids.find(string(cid));
            if (findcid == matched_cids.end()) // exists
            {
                matched_cids.insert(string(cid));
                RELEASECODE(printf("%s\t%s\ttrue\n", docid.c_str(), cid);)
            }

            num_matched_words ++;
        }


        fprintf(stderr, "[%s]  SCORE: %d / %d (%f), matches: %d / %d\n", docid.c_str(), score, n2, float(score) / n2, num_matched_words, n1);

        
        delete [] edges;
        delete edge_num;
        
    }
    
}

