#include <iostream>
#include <fstream>
#include <string>
#include <bits/stdc++.h>
#include <regex>


using namespace std;

/* The purpose of this file is to build a reverse index that takes a word and spits out the files that
 contain it. To do this properly, we need some custom functions. We are building those now.  */
void add_filename_to_map(unordered_map<string,vector<string>> * ptr_wordMap, string word, string fileName){
// this function adds the filename vector to ptr_wordMap
// if the vector doesn't exist it creates it, else it adds the new enitry to the existing vector
	if(ptr_wordMap->count(word)>0){ //if wordMap contains the key word
		vector<string> * ptr_fileNameVec;
		ptr_fileNameVec = &((*ptr_wordMap)[word]);
		if (!(std::find(ptr_fileNameVec -> begin(), ptr_fileNameVec -> end(), fileName) != ptr_fileNameVec -> end())) //if not in vector (this is slow and bad but okay..)
		//ideally there should be a hash map or something where the searching is not O(n) it is O(1). I guess the old way was better...
		{
		  	ptr_fileNameVec -> push_back(fileName);
		}
	}
	else{ //if wordMap does not contain key word
		vector<string> fileNameVec;
		fileNameVec.push_back(fileName);
		(*ptr_wordMap)[word] = fileNameVec;
	}

}


void printWordMap(unordered_map<string,vector<string>> * ptr_wordMap){
	ofstream outputFile;
	outputFile.open("outfile.txt");

	cout << "===========PRINTING WORD MAP===============\n\n\n\n\n";
	for (auto fileMapKV : *ptr_wordMap){
		cout << "key: "  << fileMapKV.first << " FILENAME: " << endl;
		outputFile << "key: "  << fileMapKV.first << " FILENAME: " << endl;
		for (auto fileName: fileMapKV.second){
			cout << fileName << "    ";
			outputFile << fileName << "    ";
		}
		cout << "\n";
	}
}

void write_wordMap_to_file(string fileName, unordered_map<string,vector<string>> * ptr_wordMap){
	ofstream wordMapFile;
	wordMapFile.open(fileName);
	for (auto fileMapKV : *ptr_wordMap){
		wordMapFile << fileMapKV.first << " ";
		for (auto fileName: fileMapKV.second){
			wordMapFile << fileName << " ";
		}
		wordMapFile << "\n";
	}
	wordMapFile.close();
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
	//printWordMap(ptr_wordMap);
}











int main(void){

	fstream fileListFile;
	fstream cityPlanFile;
	vector<string> fileNameList;

	fileListFile.open("FILELIST.txt"); //FILELIST.txt contains a list of all of the cities FILELIST_SHORT.txt contains only a 3
    if (fileListFile.is_open()){   //checking whether the file is open
	    string line; //defines a new line variable
	    while(getline(fileListFile, line)){ //read data from file object and put it into string.
	    	//cout << line <<"\n";
	    	fileNameList.push_back(line);
	    }
	}



	unordered_map<string, vector<string>> wordMap; //maps the words to the files that contain those words

	for (string fileName: fileNameList){
		cityPlanFile.open(fileName,ios::in); //open a file to perform read operation using file object
	    cout << "reading file: " << fileName << endl;
	    if (cityPlanFile.is_open()){   //checking whether the file is open
		    string line; //defines a new line variable
		    while(getline(cityPlanFile, line)){ //read data from file object and put it into string.
					char y = 0xA0;
					std::replace(line.begin(), line.end(), y, ' ');
					std::replace(line.begin(), line.end(), '/', ' ');
		    	istringstream ss(line); //creates an string stream object
		    	do{
		         	string word;
		         	ss >> word;
		         	//bool contains_non_alpha = !std::regex_match(word, std::regex("^[A-Za-z]+$")); //removes bad keys from hash map
		         	//if(contains_non_alpha){
		         		//continue;
		         	//}
							std::for_each(word.begin(), word.end(), [](char & c){
    						c = ::tolower(c);
							});
							word.resize(remove_if(word.begin(), word.end(),[](char x){return !isalnum(x) && !isspace(x);})-word.begin());
		         	if(!any_of(word.begin(), word.end(), ::isdigit)){ //this removes number digits from the words should be expanded
		         		add_filename_to_map(&wordMap,word, fileName);
		         		//cout << word << "\n";
		         	}
		         	else{
		         		//cout << "this was called" << "\n";
		         	}

		         } while(ss);

		    }
	    	cityPlanFile.close(); //close the file object.
		}
	}
	//printWordMap(&wordMap);
	write_wordMap_to_file("../../Cpp/toRun/test.txt",&wordMap);
	//unordered_map<string, vector<string>> new_wordMap;
	//read_wordMap_to_file("test.txt",&new_wordMap);
	//printWordMap(&new_wordMap);

	return 0;
}
