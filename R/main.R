rm( list = ls()); 
gc();

library(shiny)
library(leaflet)
load_data_path = file.path('data_load_and_clean','load_data.R')
source(load_data_path)
search_func_path = file.path('data_load_and_clean','R_phrase_search_func.R')
source(search_func_path)
runApp(file.path('R_shinny'))
       