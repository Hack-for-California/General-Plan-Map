#This 
library(tidyverse)  # imports plotting and other key data analysis packages 
library(leaflet)  # makes javascript visual maps 
library(sf)  # Support for simple features, a standardized way to encode spatial vector data.
library(rgdal)  # reads shapefiles
ca_place_path = file.path("..","data","ca-places-boundaries")
print(ca_place_path)
city <- readOGR(ca_place_path,"CA_Places_TIGER2016", stringsAsFactors = FALSE)  # reads shape files 
city <- spTransform(city, CRS("+proj=longlat +datum=WGS84"))  # changes corrdinate reference system
city_sf <- st_as_sf(city)  # converts st object to an sf object 
city_sf_fixed <- 
  city_sf %>%
  filter(LSAD %in% c(25, 43, 57)) %>%  # currently not doing anything since all rows are classed as one of these three (city, town, CDP, or Census Designated Place)
  mutate(FILE = paste("City_", NAME, ".txt", sep = ""))
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


file_names_path = file.path("..","data","fileNames.csv")
file_names <- read.csv(file_names_path)
names(file_names) <- "FILE"  # fixes bug with wrongly titled file_names column 
city_sf_final <- city_sf_fixed  %>% right_join(file_names, by = "FILE") 
city_sf_no_files <- city_sf_fixed 
n <- city_sf_final %>% filter(is.na(NAME))

city_sf_final$filepath_2 <- paste("https://raw.githubusercontent.com/Hack-for-California/General-Plan-Map/master/data/plan_text/", city_sf_final$FILE, sep="")
new_city <- city_sf_final

city_sf_final$search_matching = sapply(strsplit(city_sf_final$filepath_2, split = "/data/"), FUN = function(x){x[2]})
search_wrapper <- function(search_term){
  return(mySearch(search_term))
}
