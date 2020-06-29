#include <iostream>
#include <fstream>
#include <string>
#include <bits/stdc++.h> 

using namespace std;

/* The purpose of this file is to test out the loading procedure */
void add_linenumber(unordered_map<string,vector<int>> * ptr_filenameMap, string fileName, int lineNumber){
// this function adds the linenumber vector to ptr_filenameMap
// if the vector doesn't exist it creates it, else it adds the new enitry to the existing vector 
	if(ptr_filenameMap->count(fileName)>0){ //if filemap contains the key filename
		vector<int> * ptr_lineNumVec;
		ptr_lineNumVec = &((*ptr_filenameMap)[fileName]);
		ptr_lineNumVec -> push_back(lineNumber);
	}
	else{ //if filemap does not contain key filename 
		vector<int> lineNumberVec; 
		lineNumberVec.push_back(lineNumber);
		(*ptr_filenameMap)[fileName] = lineNumberVec; 
	}

}

void printWordMap(unordered_map<string, unordered_map<string,vector<int>>> wordMap){
	cout << "===========PRINTING WORD MAP===============\n\n\n\n\n";
	for (auto fileMapKV : wordMap){
		cout << "\nword: " << fileMapKV.first << "\n";
		for (auto lineVectorKV :fileMapKV.second){
			cout << "filename: " << lineVectorKV.first << "\n";
			for (auto lineNumKV: lineVectorKV.second){
				cout << "Line #: "<<lineNumKV << ", " ;//<< to_string(lineNumKV.second) << "\n";
			}
			cout << "\n";
		}
			/*for (int lineNumber: lineNumberVec){
				cout << lineNumber << "\n" ; 
			}*/
		//}
	}
}

vector<string> find_cities(unordered_map<string, unordered_map<string,vector<int>>>* pnt_wordMap,string word){ //vector<stirng> 
    cout << "===========FINDING CITIES===============\n\n\n\n\n";
    vector<string> cityNameVector;
    //unordered_map<string,vector<int>> * pnt_fileNameMap = &((*pnt_wordMap)[word]);
    for (auto fileNameKV: (*pnt_wordMap)[word]){
    	string key = fileNameKV.first;
    	cityNameVector.push_back(key);
    	cout << key << "\n";
    }
	return cityNameVector;
}

int main(void){
	fstream fileListFile; 
	fstream cityPlanFile;
	vector<string> fileNameList;

	fileListFile.open("FILELIST.txt");
    if (fileListFile.is_open()){   //checking whether the file is open
	    string line; //defines a new line variable 
	    while(getline(fileListFile, line)){ //read data from file object and put it into string.
	    	//cout << line <<"\n";
	    	fileNameList.push_back(line);
	    }
	} 


	/*fileNameList.push_back("b.txt");
	fileNameList.push_back("a.txt");
	fileNameList.push_back("City_Woodland.txt");*/

	unordered_map<string, unordered_map<string,vector<int>>> wordMap; //maps th words to filename hashmap with line numbers 

	for (string fileName: fileNameList){
		cityPlanFile.open(fileName,ios::in); //open a file to perform read operation using file object
	    int lineNumber = 1; 
	    cout << "reading file: " << fileName << "\n";
	    if (cityPlanFile.is_open()){   //checking whether the file is open
		    string line; //defines a new line variable 
		    while(getline(cityPlanFile, line)){ //read data from file object and put it into string.
		    	istringstream ss(line); //creates an string stream object 
		    	do{
		         	string word;
		         	ss >> word; 
		         	if(wordMap.count(word)>0){ //check to see if wordMap contains word 
		         		unordered_map<string,vector<int>> * pnt_fileMap;
		         		pnt_fileMap = &wordMap[word];
		         		add_linenumber(pnt_fileMap,fileName,lineNumber);

		         	}

		         	else{
		         	    unordered_map<string,vector<int>> newFileMap; //filename map pointer 
		         		add_linenumber(&newFileMap, fileName, lineNumber); //add linenumber to newFilemap 
		         		wordMap[word] = newFileMap; //store it in the word map 
		         	}
		         	unordered_map<string,vector<int>> tmp; 



		         	//cout << word << "\n";
		         } while(ss);

		         lineNumber++;  
		    }
	    	cityPlanFile.close(); //close the file object.
		}
	}
	//printWordMap(wordMap);
	find_cities(&wordMap,"housing plan");
	return 0; 
}