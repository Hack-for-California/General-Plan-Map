	// [[Rcpp::plugins(cpp11)]]
	#include <iostream>
	#include <fstream>
	#include <string>
	#include <unordered_map> 
	#include <vector>
	#include <sstream>
	#include <cstring>
	#include <algorithm> // for set_intersection

	using namespace std;

	void printWordMap(unordered_map<string,vector<string>> * ptr_wordMap){
	  cout << "===========PRINTING WORD MAP===============\n\n\n\n\n";
	  for (auto fileMapKV : *ptr_wordMap){
	    cout << "key: "  << fileMapKV.first << " FILENAME: " << endl;
	    for (auto fileName: fileMapKV.second){
	      cout << fileName << "    "; 
	    }
	    cout << "\n";
	  }
	} 

	void read_wordMap_to_file(string fileName, unordered_map<string,vector<string>> * ptr_wordMap){
	  //this function loads a wordmap from a file 
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
	        }
	        else{ //if not on the first word of the line 
	          if (word.compare("")!=0){ //prevents blank words from being added 
	            (&((*ptr_wordMap)[key]))->push_back(word);
	          }
	        }
	        i++;
	      } while(ss);
	    }
	  } 
	  wordMapFile.close();
	}

	// [[Rcpp::export]]
	vector<string> mySearch(string search_term){
	  unordered_map<string, vector<string>> wordMap;
	  read_wordMap_to_file("C:\\Users\\dexte\\Box\\hack_ca\\General_Plan_Map_Clean\\Cpp\\toRun\\test.txt",&wordMap);
	  string term;
	  
	  /* Need to figure out how to efficently resize result everytime! */
	  //vector<string> prevResult, currResult, result(500);
	  vector<string> *prevResult = new vector<string>(); 
	  vector<string> *currResult = new vector<string>(); 
	  vector<string> *result = new vector<string>(); 
	  istringstream s_line(search_term);
	  int count = 0;
	  //int newsize;
	  
	  while(s_line >> term){
	    cout << term << endl;
	    if (count == 0) {
	      printf("Hey we're in if statement\n");
	      result = &wordMap[term];
	    } else {
	      printf("Hey we're in else statement\n");
	      prevResult = result;
	      currResult = &wordMap[term];
	      //newsize = currResult->size();
	      //cout << "size is: " << newsize << endl;
	      //result->resize(newsize);
	      
	      /* need to figure out how to resize result AND have it overwrite what's already in result */
	      set_intersection(prevResult->begin(), prevResult->end(), 
	                       currResult->begin(), currResult->end(),
	                       result->begin());
	    }
	    count++;
	  } 
	  
	//  return wordMap[search_term];
	  cout << search_term << endl;
	  return *result;
	}
