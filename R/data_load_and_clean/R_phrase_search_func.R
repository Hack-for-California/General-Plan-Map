library(stringr)
library(Rcpp)

url <- "https://raw.githubusercontent.com/Hack-for-California/General-Plan-Map/master/plan_text/"
input <- "and"

processFile = function(filepath, input) {
  con = file(filepath, "r")
  while (TRUE) {
    line = readLines(con, n = 1, warn = FALSE)
    if (length(line) == 0 ) {
      close(con)
      return (0)
    }
    if (str_detect(line, input)){
      close(con)
      return (1)
    }
  }
}

searchFile = function(filepath,input){
  print("func filepath")
  print(filepath)
  toReturn = paste("Link to General Plan: ", filepath)
  return(toReturn) 
  
}


Cpp_search_function_filepath = file.path('..','Cpp','toRun','basicSearch.cpp')



sourceCpp(Cpp_search_function_filepath)

search_wrapper <- function(search_term){
  if(search_term == ''){
    search_term = 'the'
  }
  return(mySearch(search_term))
}