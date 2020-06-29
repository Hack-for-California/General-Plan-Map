#include <iostream>
#include <fstream>
#include <string>
#include <bits/stdc++.h> 

using namespace std;

int main(void){

   unordered_map<string, unordered_map<string,vector<string>>>  vectorTest;
   vector<string> adsf;
   adsf.push_back("Toby");
   vectorTest["dog"] = adsf; 
   string wordToAdd = "dog";
   string bookName = "Boomer"; 
   
   if(vectorTest.count(wordToAdd)>0){
      vector<string> * tmpVectorPointer;
      tmpVectorPointer = &vectorTest[wordToAdd];
      tmpVectorPointer->push_back(bookName);
      for (auto a : *tmpVectorPointer)
         cout << "\n" << a << "\n";   
      cout << "\n DONE WITH FIRST IF STATEMENT \n";
   }
   if(vectorTest.count(wordToAdd)>0){
      vector<string> tmpVector;
      tmpVector = vectorTest[wordToAdd];
      tmpVector.push_back(bookName);
      for (auto a : tmpVector)
         cout << "\n" << a << "\n"; 

      //cout << tmpVector[0] << "\n" tmpVector[1] << "\n";

   }
   /*
   
   if(1){ //contains word 
      //vector<string> tmpVector;
      //tmpVector = vectorTest[wordToAdd];
      //tmpVector.push_back(bookName);
      cout << "if statement exicuted"; 
   }
   else{
      vector<string> newVector;
      newVector.push_back(bookName);
      vectorTest[wordToAdd] = newVector;
   }

   vector<string> myNewVector; 
   myNewVector.push_back("toby");

   vectorTest["dog"] = myNewVector;
   cout << vectorTest["test"][0] << "\n";
   */
	return 0; 
}

