library(stringr)
library(Rcpp)

#Source C++ word search function
Cpp_search_function_filepath = file.path('..','search_cpp','basic_search.cpp')
sourceCpp(Cpp_search_function_filepath)

#Search for term 
search_wrapper <- function(search_term){
  if(search_term == ''){
    search_term <- 'the'
  }
  return(my_search(search_term))
}

# Previous attempts
# url <- "https://raw.githubusercontent.com/Hack-for-California/General-Plan-Map/master/data/plan_text/"
# input <- "and"
# processFile = function(filepath, input) {
#   con = file(filepath, "r")
#   while (TRUE) {
#     line = readLines(con, n = 1, warn = FALSE)
#     if (length(line) == 0 ) {
#       close(con)
#       return (0)
#     }
#     if (str_detect(line, input)){
#       close(con)
#       return (1)
#     }
#   }
# }