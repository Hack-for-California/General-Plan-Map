// [[Rcpp::plugins(cpp11)]]
#include <iostream>
#include <fstream>
#include <string>
#include <bits/stdc++.h> 

//using namespace Rcpp;
using namespace std;




void printWordMap(unordered_map<string,vector<string>> * ptr_wordMap){
	//ofstream outputFile;
	//outputFile.open("outfile.txt");

	cout << "===========PRINTING WORD MAP===============\n\n\n\n\n";
	for (auto fileMapKV : *ptr_wordMap){
		cout << "key: "  << fileMapKV.first << " FILENAME: " << endl;
		//outputFile << "key: "  << fileMapKV.first << " FILENAME: " << endl;
		for (auto fileName: fileMapKV.second){
			cout << fileName << "    "; 
			//outputFile << fileName << "    "; 
		}
		cout << "\n";
	}
} 


// [[Rcpp::export]]
void read_wordMap_to_file(string fileName){ //, unordered_map<string,vector<string>> * ptr_wordMap){
	//this function loads a wordmap from a file 
	//unordered_map<string,vector<string>>  * ptr_wordMap; //delete if add extra argument 
	unordered_map<string,vector<string>> wordMap;
	auto ptr_wordMap = &wordMap;
	ifstream wordMapFile;
    wordMapFile.open(fileName); 
	if(wordMapFile.is_open()){
		string line; 
		while(getline(wordMapFile, line)){
		int i = 0; 
		string key;

		istringstream ss(line);
		 	do{
	         	string word;
	         	ss >> word; 
	         	vector<string> newFileNameVec; 
	         	if(i==0){ // if on the first word in the line 
	         		key = word;
	         		(*ptr_wordMap)[key] = newFileNameVec; //add key and the new vector to the file 
	         		//cout << "new key is:" << word << "\n";
	         	}
	         	else{ //if not on the first word of the line 
	         		if (word.compare("")!=0){ //prevents blank words from being added 
		         		(&((*ptr_wordMap)[key]))->push_back(word);
		         		//cout << "new filename is:" << word << "a\n";
	         		}
	         	}

 	    		i++;

	         } while(ss);

		}

	} 
	wordMapFile.close();
	printWordMap(ptr_wordMap);
}









