library(tidyverse)  # imports plotting and other key data analysis packages 
library(leaflet)  # makes javascript visual maps 
library(sf)  # Support for simple features, a standardized way to encode spatial vector data.
library(rgdal)  # reads shapefiles

#Read city shape files and convert to sf object
ca_place_path = file.path("..","data","ca-places-boundaries") #folder with city shapefiles
print(ca_place_path)
city <- readOGR(ca_place_path,"CA_Places_TIGER2016", stringsAsFactors = FALSE)  # reads shape files 
city <- spTransform(city, CRS("+proj=longlat +datum=WGS84"))  # changes corrdinate reference system
city_sf <- st_as_sf(city)  # converts st object to an sf object 

#Add files names to city shapefile data frame
city_sf_fixed <- 
  city_sf %>%
  filter(LSAD %in% c(25, 43, 57)) %>%  #Filters to geography type; currently not doing anything since all rows are classed as one of these three (city, town, CDP, or Census Designated Place)
  mutate(FILE = paste("City_", NAME, ".txt", sep = "")) #Creates a new column with the link to the general plan text

#Edits the file names in the FILE column to match the general plan file names
city_sf_fixed$FILE <- gsub("Angels", "Angels Camp", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("Gustine", "Gustine City", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("Truckee", "Town of Truckee", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("Tustin", "Tustin Foothills", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("Windsor", "Town of Windsor", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("Yreka", "Yreka City", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("St. ", "Saint ", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub(" \\(.*\\)", "", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("ñ", "n", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("-", "_", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub("de ", "De ", city_sf_fixed$FILE)
city_sf_fixed$FILE <- gsub(" ", "_", city_sf_fixed$FILE)

#Reads a list of general plan file names in our database into data frame
file_names_path = file.path("..","data","fileNames.csv")
file_names <- read.csv(file_names_path)
names(file_names) <- "FILE"  #Sets file column name to match column name in city_sf_fixed

#Joins city_sf_fixed to file_names in order to filter out those rows in the city shape file data frame for which we do not have general plans
city_sf_final <- city_sf_fixed  %>% right_join(file_names, by = "FILE") 

#Adds columns for file paths
city_sf_final <- 
  city_sf_final %>%
  mutate(filepath_2 = paste("https://raw.githubusercontent.com/Hack-for-California/General-Plan-Map/master/data/plan_text/", city_sf_final$FILE, sep=""),
         search_matching = sapply(strsplit(filepath_2, split = "/data/"), FUN = function(x){x[2]}))

