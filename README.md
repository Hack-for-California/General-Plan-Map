# General-Plan-Map

## How to Access

You can access a working version of this application [here](http://critical-data-analysis.org/shiny/general-plan-map/R/).

## About


## Goals

## Contributors

* [Catherine Brinkley](https://humanecology.ucdavis.edu/catherine-brinkley), Project Lead
* [Lindsay Poirier](https://sts.ucdavis.edu/people/lpoirier), Critical Data Analysis Lead
* Dexter Antonio, Lead Developer

## How to Contribute

1. File an issue via this repo's [issue queue](https://github.com/Hack-for-California/General-Plan-Map/issues).

2. Write code to fix issues or to create new features. When contributing code, please be sure to:

  * Fork this repository, modify the code (changing only one thing at a time), and then issue a pull request for each change.
  * Follow the project's coding style (using K&R-style indentation and bracketing, commenting above each feature, and using snake case for variables).
  * Test your code locally before issuing a pull request.
  * Clearly state the purpose of your change in the description field for each commit.

## Architecture

The code for the shiny app is stored in [R](./R). Running app.R in this folder launches the app, 
loading the CA city shapefiles into a data frame via load_data.R in the [R/data_load_and_clean](./R/data_load_and_clean) 
folder and calling on ui.R and server.R in the [R/shiny_app](./R/shiny_app) folder. 

ui.R includes all of the code for the front end of the app, including the front-end text, links to the stylesheet, and the basic layout of the page. 

server.R includes the code for the backend. server.R is responsible for loading the map, and observes and calls functions when a user clicks the Search button, 
the Clear button, or a polygon on the map. 

When a user clicks on the Search button, server.R calls on R_phrase_search_func.R in the [R/data_load_and_clean](./R/data_load_and_clean) folder,
which calls on basic_search.cpp in the [search_cpp](./search_cpp) folder. 

basic_search.cpp reads in word_map.txt also stored in the [search_cpp](./search_cpp) folder. 
word_map.txt maps every identifiable word in the general plans to the file names of the general plans in which those words can be found. Taking 
the user's search term as an input, basic_search.cpp locates the word in the map and returns the file names of all general plans in which that word can be found.
server.R then filters to the city's associated with those plans on the map. 

word_map.txt is created with a C++ called containsWordReverseIndexer0.1.cpp in the [indexing_cpp](./indexing_cpp) folder.

### R Package Dependencies

* [tidyverse](https://www.tidyverse.org/)
* [shiny](https://shiny.rstudio.com/)
* [leaflet](https://rstudio.github.io/leaflet/)
* [sf](https://r-spatial.github.io/sf/articles/sf1.html)
* [rgdal](https://cran.r-project.org/web/packages/rgdal/rgdal.pdf)
* [Rcpp](http://www.rcpp.org/)

## Copyrights

Please see [license](https://github.com/Hack-for-California/General-Plan-Map/blob/master/LICENSE) file for details.

## Cite As

Brinkley, C; Poirier, L; Antonio, D (2020) California City General Plan Database Mapping Tool. [http://critical-data-analysis.org/shiny/general-plan-map/R/](http://critical-data-analysis.org/shiny/general-plan-map/R/)

## Have Questions?
Contact [hack-for-california@ucdavis.edu](mailto:hack-for-california@ucdavis.edu)
