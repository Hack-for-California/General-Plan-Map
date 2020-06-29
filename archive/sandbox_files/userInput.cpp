#include <iostream>
#include <fstream>
#include <string>
#include <bits/stdc++.h> 

using namespace std;

int main(void){
   fstream newfile;
   /*newfile.open("example.txt",ios::out);  // open a file to perform write operation using file object
   if(newfile.is_open()) //checking whether the file is open
   {
      newfile<<"Tutorials point \n";   //inserting text
      newfile.close();    //close the file object
   }*/

   unordered_map<int, string>  int2String{ {3,"three"},{2,"two"},{1,"one"},{5,"five"},{6,"six"},{4,"four"},{7,"seven"} };
   int2String[3] = "THREE!";

   unordered_map<string, vector<string>>  vectorTest;
   vector<string> myNewVector; 
   myNewVector.push_back("I like dogs");
   vectorTest["test"] = myNewVector;
   cout << vectorTest["test"][0];

   int2String[3] = "THREE!";
   cout << int2String[3];
   newfile.open("example.txt",ios::in); //open a file to perform read operation using file object
   if (newfile.is_open()){   //checking whether the file is open
      string line; //defines a new line variable 
      while(getline(newfile, line)){ //read data from file object and put it into string.
         istringstream ss(line); //creatse an ss object 
         do{
         	string word;
         	ss >> word; 
         	cout << word << "\n";
         } while(ss); 

      }
      newfile.close(); //close the file object.
   }

	return 0; 
}

