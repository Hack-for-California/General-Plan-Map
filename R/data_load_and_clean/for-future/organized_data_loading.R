#this file loads housing data from an excel spreadsheet 
#this could be useful for adding a second layer or data analysis 

file_names <- 
  read.csv("fileNames.csv")
name = read.csv(file="..\\housing_data.csv",header=TRUE,stringsAsFactors = FALSE)
colnames(name) = c("JURISDICTION", "VLI RHNA", "VLI PERMITS", "VLI (DR) UNITS", "VLI (NDR) UNITS", "VLI REMAIN UNITS", "VLI % COMPLETE", "Prorated VLI RHNA", "Excess VLI", "LI RHNA", "LI PERMITS", "LI (DR) UNITS", "LI (NDR) UNITS", "LI  REMAIN UNITS", "Lower Permits", "Lower Remain", "LI % COMPLETE", "% Lower Complete", "MOD RHNA", "MOD PERMITS", "MOD REMAIN UNITS", "MOD % COMPLETE", "ABOVE MOD RHNA", "ABOVE MOD PERMITS", "ABOVE MOD REMAIN UNITS", "ABOVE MOD % COMPLETE", "RHNA TOTAL", "TOTAL PERMITS", "TOTAL RHNA REMAIN", "PRORATION FACTOR")
name$JURISDICTION = tolower(name$JURISDICTION)
city_sf_newnames<-city_sf_fixed
city_sf_newnames$NAME = tolower(city_sf_fixed$NAME)
city_all = merge(name,city_sf_newnames,by.x="JURISDICTION",by.y = "NAME", all.y=TRUE)

names(file_names) <- "FILE" #fixes bug with wrongly titled file_names column 
city_sf_final <- city_sf_fixed  %>% right_join(file_names, by = "FILE") 
city_sf_no_files <- city_sf_fixed 
n <- city_sf_final %>% filter(is.na(NAME