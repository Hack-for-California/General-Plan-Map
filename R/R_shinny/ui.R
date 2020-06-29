ui <- fluidPage(tags$head(includeCSS("../style/style.css")),
                div(class="sidebar-panel",
                    sidebarPanel(tags$h1("California City General Plan Database Mapping Tool"),
                                 tags$p("The purpose of this website is to enable users to access, 
                                       query, compare, and spatially visualize general plans in 
                                       cities across California."), 
                                 tags$hr(),
                                 tags$p("Instructions: Enter a single word search term 
                                       into the textbox, and click Search to query across the plans. 
                                       The map will highlight cities with general plans that include the search term. 
                                       Click a city on the map for links to the text of the city's plan. 
                                       Plans were added in 2017, and we are in the process of adding the updates."),
                                 tags$a(href = "https://docs.google.com/forms/d/e/1FAIpQLSeCpD1Dil06c8tuSLnDqHp9W_6zK3S50ho4eGQtM4MyBhYM4g/viewform?usp=sf_link", "Please leave us feedback here."),  
                                 textInput("search", "", placeholder = "Enter Search Term"),
                                 actionButton("do", "Search"),
                                 actionButton("clear_map", "Clear Search"),
                                 #selectizeInput('city', label = NULL, choices = city_sf$NAME,options = list(create = TRUE)),
                                 tags$hr(),
                                 tags$p("Please cite: Brinkley, C; Poirier, L; Antonio, D (2020) California City General Plan Database Mapping Tool. http://critical-data-analysis.org/shiny/general-plan-map/R/"),
                                 uiOutput("test_label"),
                                 uiOutput("city_selected"))), 
                mainPanel(leafletOutput("mymap"), height=50),
                mainPanel(uiOutput("search_result"), 
                          DT::dataTableOutput("search_result_table")) 
                
                )