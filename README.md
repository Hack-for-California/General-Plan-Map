# General-Plan-Map

## How to Access

You can access a working version of this application [here](http://critical-data-analysis.org/shiny/general-plan-map/R/).

## About

Each city and county in California is required to produce a General Plan, a document that outlines and commits local governments to long-term development goals. Planning laws in the State of California mandate that every General Plan address a common set of issues, including Land Use, Conservation, and Housing. However, such laws do not specify where in the General Plan such issues need to be addressed or the format of the Plan overall. Thus, while General Plans offer the most comprehensive blueprint for future visioning of cities and counties throughout California, the structure and format of the Plans vary considerably across cities and counties. This makes it difficult to readily compare planning approaches across the state, to comparatively evaluate progress towards planning goals, and to set benchmarks for policy success. 
 
This project is developing a platform for readily querying and extracting snippets of information about issues such as planned housing across all General Plans. Currently, there are no states that have such a public database for querying General Plans state-wide. The platform is expected to become a key policy implementation and enforcement infrastructure for the California OPR, a resource for community developers in collaborative planning, and a valuable information source for community members and researchers. 

### The Tool

The General Plan Map provides access to the text of all California city General Plans and enables users to query for a single search term to determine the plans in which that term is referenced. Upon searching, the tool filters a map to the cities in CA with General Plans that reference the word, offering a geospatial representation of the term's use. The tool also links to the plans that reference the term. Users can click through to the plans and search within the page for the term. 

### Some Notes and Caveats

* Curently, the search function searches for a term from a corpus of words that have been extracted from each of the plans. In that corpus, numbers and special characters (e.g. -,(,),\*,%,$,#,",',:) have all been stripped. This means that if you wanted to search for something like "community-oriented" you should instead search for "communityoriented". It also means that terms like "4-lane" or "3-year" in the General Plans will appear in the corpus as "lane" and "year".
* In that corpus, words containing "/" have been separated into the words appearing before and after the "/". This means that if a plan contains the term "land/water/air", the plan would appear in a search for "land", "water", or "air" but not a search for "land/water/air".
* When words span two lines in the plan (continued with a "-"), the full word will not appear in the corpus. Instead, the two word fragments will appear in the corpus. 
* Some text in the General Plans, particularly text in textboxes, captions, and charts, did not properly parse when we converted the General Plan PDFs to text files. If this was the case, these terms will not appear in the corpus. The tool also cannot capture any text that appears in images in the Plans.

### Longer-Term Goals

* Archive historical general plans for each city in order to be able to track changes in plans over time
* Add county plans to the map, and allow users to toggle between the two
* Expand search functionality beyond a single word towards phrases
* Link to PDFs of the general plans vs. unformatted text
* Streamline the addition of new plans to the database

## Contributors

* [Catherine Brinkley](https://humanecology.ucdavis.edu/catherine-brinkley), Project Lead
* [Lindsay Poirier](https://sts.ucdavis.edu/people/lpoirier), Critical Data Analysis Lead
* Dexter Antonio, Lead Developer
* Makena Dettmann
* Margaret Riley

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
