ui <- fluidPage(
  titlePanel("California General Plan Mapping"),
  sidebarPanel("Welcome to the California General Plan Mapping project!
               The purpose of this website is to enable users to access, query, compare, 
               and spatially visualize general plans in cities across California.
               Enter a search term into the textbox, and click Search to query across the plans.
               The map will highlight cities with general plans that include the search term.
               Click a city on the map for links to the text of the city's plan.",  
               textInput("search", "", placeholder = "Enter Search Term"),
               actionButton("do", "Search"),
               actionButton("clear_map", "Clear Search"),
               #selectizeInput('city', label = NULL, choices = city_sf$NAME,options = list(create = TRUE)),
               uiOutput("test_label"),uiOutput("city_selected")), 

  mainPanel(leafletOutput("mymap"), height=50),
  mainPanel(uiOutput("search_result")), tableOutput('search_result_table'))