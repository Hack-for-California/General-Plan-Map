library(Rcpp)
sourceCpp('basicSearch.cpp')
results <- mySearch("housing")

sapply(strsplit(city_sf_final$filepath, split = "/master/"), FUN = function(x){x[2]})
