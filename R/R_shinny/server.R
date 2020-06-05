server <- function(input, output, session) {
  
  points <- eventReactive(input$recalc, {
    cbind(rnorm(40) * 2 + 13, rnorm(40) + 48)
  }, ignoreNULL = FALSE)
  
  t_label <- ""
  output$city_selected <- renderUI({HTML(input$city)})
  output$test_label <- renderUI({HTML(t_label)})
  output$search_result <- renderUI({HTML('<header style="font-size:30px">Search Result</header>')})
  
  leafletProxy("mymap", session)
  
  observeEvent(input$do, {print("Search for things button clicked"); search_for_things();})

  observeEvent(input$clear_map, {print("clear map button clicked"); clear_map();})
  output$mymap=renderUI({
    leafletOutput('myMap', width = "200%", height = '500%')
  })
  
  output$mymap <- renderLeaflet({
    leaflet() %>%
      addProviderTiles(providers$CartoDB.Positron) %>%
      addPolygons(data = city_sf_final, 
                  label = ~NAME,
                  color = "#444444",
                  weight = 0.5,
                  smoothFactor = 0.8,
                  opacity = 1.0,
                  fillOpacity = 0.5,
                  layerId = ~NAME,
                  highlightOptions = highlightOptions(color = "white",
                                                      weight = 1,
                                                      bringToFront = TRUE), 
                  labelOptions = labelOptions(
                    style = list("font-weight" = "normal",
                                 padding = "3px 8px"),
                    textsize = "10px",
                    direction = "auto"))
  })
  
  search_Rcpp <- reactive({
    search_results = search_wrapper(input$search)
    search_city_bool = city_sf_final$search_matching %in% search_results
  })
  
  search_for_things <- reactive(  {
    print("search_for_things is called")
    #search_results <- sapply(X = new_city$filepath[1:10], FUN = processFile, input = input$search)
    #city_sf_final$search <- rep(0,nrow(city_sf_final))
    #city_sf_final$search[1:10] = search_results
    search_results = search_wrapper(input$search)
    search_city_bool = city_sf_final$search_matching %in% search_results
    city_sf_final$search = search_city_bool
    d <-subset(city_sf_final, city_sf_final$search == 1)
    
    copy_pos_search = data.frame(d)
    table_display = select(copy_pos_search,c('NAMELSAD','filepath_2'))
    table_display$filepath_2 = paste0("<a href='",table_display$filepath_2,"' target='_blank'>",table_display$filepath_2,"</a>")
    names(table_display) = c('Name', 'Link')
    #copy_city_sf_final = sapply(copy_city_sf_final,unlist)
    output$search_result_table <- renderTable(table_display, sanitize.text.function = function(x) x)
    
    if(NROW(d)==0){
      return 
    }
    toClear = subset(city_sf_final, city_sf_final$search == 0)
    #things for highlighting selected cities 
    leafletProxy("mymap", session) %>% addPolygons(data = d, 
                                                   layerId = ~NAME,
                                                   label = ~NAME,
                                                   color = "#444444",
                                                   weight = 0.5,
                                                   smoothFactor = 0.8,
                                                   opacity = 1.0,
                                                   fillOpacity = 1,
                                                   fillColor = 'blue',
                                                   highlightOptions = highlightOptions(color = "gray",
                                                                                       fillColor = "gray",
                                                                                       weight = 3,
                                                                                       bringToFront = TRUE), 
                                                   labelOptions = labelOptions(
                                                     style = list("font-weight" = "normal",
                                                                  padding = "3px 8px"),
                                                     textsize = "10px",
                                                     direction = "auto"))
    
    
    leafletProxy("mymap", session) %>% addPolygons(data = toClear, 
                                                   layerId = ~NAME,
                                                   label = ~NAME,
                                                   color = "#444444",
                                                   weight = 0.5,
                                                   smoothFactor = 0.8,
                                                   opacity = 1.0,
                                                   fillOpacity = 1,
                                                   fillColor = 'white',
                                                   highlightOptions = highlightOptions(color = "yellow",
                                                                                       fillColor = "yellow",
                                                                                       weight = 3,
                                                                                       bringToFront = TRUE), 
                                                   labelOptions = labelOptions(
                                                     style = list("font-weight" = "normal",
                                                                  padding = "3px 8px"),
                                                     textsize = "10px",
                                                     direction = "auto"))
  })
  
  #to clear
  
  read_paragarph <- reactive({ #not currently in use 
    d <-subset(city_sf_final, city_sf_final$NAME == input$city)
    op <- searchFile(d$filepath,input$search)
    output$search_result <- renderUI({HTML(op)})})
  
  observeEvent(input$mymap_shape_click, { # update the location selectInput on map clicks
    p <- input$mymap_shape_click$id 
    d <- subset(city_sf_final, city_sf_final$NAME == p)
    # print(d$filepath)
    op <- searchFile(d$filepath, input = input$search)
    output$city_selected <- renderUI({HTML('<hr/><h2>',input$mymap_shape_click$id,'</h2>', op)})
    #print("d fukeoatg")
    print("d filepath")
    print(d$filepath)
  })
  
  one_city_data <- reactive({
    d <- subset(city_sf_final, city_sf_final$NAME == input$city)
    #things for highlighting selected cities 
    if(NROW(d) > 0) {
      leafletProxy("mymap", session) %>% addPolygons(data = d,
                                                 label = ~NAME,
                                                 color = "#444444",
                                                 weight = 0.5,
                                                 smoothFactor = 0.8,
                                                 opacity = 1.0,
                                                 fillOpacity = 1,
                                                 fillColor = "green",
                                                 highlightOptions = highlightOptions(color = "red",
                                                                                     fillColor = "red",
                                                                                     weight = 3,
                                                                                     bringToFront = TRUE), 
                                                 labelOptions = labelOptions(
                                                   style = list("font-weight" = "normal",
                                                                padding = "3px 8px"),
                                                   textsize = "10px",
                                                   direction = "auto")
                                                 )
      }
    })
  
  clear_map <- reactive({
    print("Clear Map")
    leafletProxy("mymap", session) %>%  addPolygons(data = city_sf_final, 
                                                       label = ~NAME,
                                                       color = "#444444",
                                                       weight = 0.5,
                                                       smoothFactor = 0.8,
                                                       opacity = 1.0,
                                                       fillOpacity = 0.5,
                                                       layerId = ~NAME,
                                                       highlightOptions = highlightOptions(color = "white",
                                                                                           weight = 1,
                                                                                           bringToFront = TRUE), 
                                                       labelOptions = labelOptions(
                                                         style = list("font-weight" = "normal",
                                                                      padding = "3px 8px"),
                                                         textsize = "10px",
                                                         direction = "auto")
                                                    )
    })
}
