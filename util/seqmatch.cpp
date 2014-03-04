//
//  main.cpp
//  test3
//
//  Created by Shan Zifei on 3/3/14.
//  Copyright (c) 2014 Shan Zifei. All rights reserved.
//


// THIS IS INCORRECT FOR NOW....

#include <iostream>
#include <fstream>
#include <string>
#include <cstdio>
using namespace std;

#define MAXLEN 100000

bool ElemMatch(const char* e1, const char* e2){
    // return e1 == e2;
  return strcmp(e1, e2) == 0;
}

char arr1[MAXLEN][256] = {0};
char arr2[MAXLEN][256] = {0};


int Match(int n1, int n2)
{
    if (n1 == 0 || n2 == 0) return 0;
    int** f = new int*[n1];
    for(int i = 0; i < n1; ++i)
        f[i] = new int[n2];
    
    // for (int i = 0; i < n1; i++) for (int j = 0; j < n2; j++) printf("%d ", f[i][j]);
    // cout << endl;
    
    // Init
    if (ElemMatch(arr1[0], arr2[0]))
        f[0][0] = 1;
    
    for (int i = 1; i < n1; i++)
        if (ElemMatch(arr1[i], arr2[0]) || f[i-1][0] == 1)
            f[i][0] = 1;
    
    
    for (int j = 1; j < n2; j++)
        if (ElemMatch(arr1[0], arr2[j]) || f[0][j-1] == 1)
            f[0][j] = 1;
    
    
    // DP
    for (int i = 0; i < n1; i++)
        for (int j = 0; j < n2; j++)
        {
            if (i + 1 < n1 && j + 1 < n2
                && ElemMatch(arr1[i+1], arr2[j+1])
                && f[i+1][j+1] < f[i][j] + 1)
                f[i+1][j+1] = f[i][j] + 1;
            
            if (i + 1 < n1 && f[i+1][j] < f[i][j]) // left shift
                f[i+1][j] = f[i][j];
            
            if (j + 1 < n2 && f[i][j+1] < f[i][j]) // right shift
                f[i][j+1] = f[i][j];
        }
    return f[n1 - 1][n2 - 1];
}


int main(int argc, const char * argv[])
{
    // cout << "Started.." << endl;
    if (argc == 3) {
        
        const char* f1 = argv[1];
        const char* f2 = argv[2];
        cout << "Reading files: " << f1 << ", " << f2 << endl;
        
        ifstream fin;
        fin.open(f1, ifstream::in);
        int n1 = 0;
        string line;
        while( std::getline( fin, line ) ) {
            strcpy(arr1[n1], line.c_str());
            // cout << line << endl;
            n1++;
        }
        fin.close();

        ifstream fin2;
        fin2.open(f2, ifstream::in);
        int n2 = 0;
        while( std::getline( fin2, line ) ) {
            strcpy(arr2[n2], line.c_str());
            // cout << line << endl;
            n2++;
        }
        fin2.close();
        cout << arr1[0] << endl;
        cout << arr2[0] << endl;
        cout << "Matches: " << endl;
        cout << Match(n1, n2) << endl;
        return 0;

    }
    else {
        // cout << "Input number of words in string x \n";
        // int n1 = 0, n2 = 0;
        // cin >> n1;
        // for (int i = 0; i < n1; i++)
        //     cin >> arr1[i];
        // cout << "Input number of words in string y \n";
        // cin >> n2;
        // for (int i = 0; i < n2; i++)
        //     cin >> arr2[i];
        
        
        // cout << "Matches: ";
        // cout << Match(arr1, arr2, n1, n2) << endl;
        return 0;
        
    }
    
}

