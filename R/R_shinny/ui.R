ui <- fluidPage(
  titlePanel("California General Plan Mapping"),
  sidebarPanel("Welcome to California General Plan Mapping project!
               The purpose of this website is to visualize California general plans. 
               Enter a search term into the textbox and press search to search the city 
               of california general plans for a certain key words",  
               textInput("search", "", placeholder = "Enter Search Term"),
               actionButton("do", "Search"),
               actionButton("clear_map", "Clear Search"),
               #selectizeInput('city', label = NULL, choices = city_sf$NAME,options = list(create = TRUE)),
               uiOutput("test_label"),uiOutput("city_selected")), 

  mainPanel(leafletOutput("mymap"), height=50),
  mainPanel(uiOutput("search_result")), tableOutput('search_result_table'))