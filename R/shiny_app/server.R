server <- function(input, output, session) {
  if (!interactive()) sink(stderr(), type = "output") # for error logging
  points <- eventReactive(input$recalc, {cbind(rnorm(40) * 2 + 13, rnorm(40) + 48)}, ignoreNULL = FALSE)
  
  #t_label <- ""
  #output$city_selected <- renderUI({HTML(input$city)})
  #output$test_label <- renderUI({HTML(t_label)})
  
  #==========================================================================================================
  #Outputs
  #==========================================================================================================
  
  output$mymap <- renderLeaflet({leaflet() %>%
                                 addProviderTiles(providers$CartoDB.Positron) %>%
                                 addPolygons(data = city_sf_final,
                                             layerId = ~NAME,
                                             label = ~NAME,
                                             color = "#444444",
                                             opacity = 1.0,
                                             weight = 0.5,
                                             smoothFactor = 1.5,
                                             fillColor = "#f8766d",
                                             fillOpacity = 0.9,
                                             highlightOptions = highlightOptions(color = "white",
                                                                                 weight = 1,
                                                                                 bringToFront = TRUE), 
                                             labelOptions = labelOptions(style = list("font-weight" = "normal",
                                                                                      padding = "3px 8px"),
                                                                         textsize = "10px",
                                                                         direction = "auto"))})
  
  
  leafletProxy("mymap", session)
  
  #==========================================================================================================
  #Events
  #==========================================================================================================
  
  observeEvent(input$do, {cat("Search for things button clicked"); 
                          #search_results <- sapply(X = new_city$filepath[1:10], FUN = processFile, input = input$search)
                          #city_sf_final$search <- rep(0,nrow(city_sf_final))
                          #city_sf_final$search[1:10] = search_results
                          search_string <- tolower(input$search)
                          search_results <- search_wrapper(search_string)
                          
                          if(str_detect(search_string, '^[A-Za-z]+$', negate = TRUE)){showModal(modalDialog(title = "Heads up!",
                                                                                                           "Please remove any numbers or special characters from the search string (e.g. community-oriented would be communityoriented)."))}
                          else{
                                if(length(search_results) == 0) {showModal(modalDialog(title = "Heads up!",
                                                                                       "Search term not found."))}
                                
                                else {output$search_result <- renderUI({HTML("<div id='search_result_header'><h2>Search Result</h2></div")})
                                      search_city_bool <- city_sf_final$search_matching %in% search_results
                                      city_sf_final$search <- search_city_bool
                                      
                                      city_row <-subset(city_sf_final, 
                                                        city_sf_final$search == 1)
                                      
                                      copy_pos_search <- data.frame(city_row)
                                      table_display <- select(copy_pos_search,
                                                             c('NAMELSAD',
                                                               'filepath_2'))
                                      
                                      table_display$filepath_2 <- paste0("<a href='",
                                                                        table_display$filepath_2,
                                                                        "' target='_blank'>",
                                                                        table_display$filepath_2,
                                                                        "</a>")
                                      cat(names(table_display))
                                      names(table_display) = c('Name', 
                                                               'Link')
                                      
                                      #copy_city_sf_final = sapply(copy_city_sf_final,unlist)
                                      
                                      output$search_result_table <- DT::renderDataTable(table_display, 
                                                                                        escape = FALSE)
                                      
                                      to_clear <- subset(city_sf_final, 
                                                       city_sf_final$search == 0)
                                      cat(dim(to_clear))
                                      cat(str(to_clear))
                                      
                                      #things for highlighting selected cities 
                                      leafletProxy("mymap", session) %>% 
                                        addPolygons(data = city_row, 
                                                    layerId = ~NAME,
                                                    label = ~NAME,
                                                    color = "#444444",
                                                    opacity = 1.0,
                                                    weight = 0.5,
                                                    smoothFactor = 1.5,
                                                    fillColor = "#00bfc4",
                                                    fillOpacity = 0.9,
                                                    highlightOptions = highlightOptions(color = "white",
                                                                                        weight = 1,
                                                                                        bringToFront = TRUE), 
                                                    labelOptions = labelOptions(style = list("font-weight" = "normal",
                                                                                             padding = "3px 8px"),
                                                                                textsize = "10px",
                                                                                direction = "auto"))
                                      if(nrow(to_clear != 0)){leafletProxy("mymap", session) %>%
                                                               addPolygons(data = to_clear,
                                                                           layerId = ~NAME,
                                                                           label = ~NAME,
                                                                           color = "#444444",
                                                                           opacity = 1.0,
                                                                           weight = 0.5,
                                                                           smoothFactor = 1.5,
                                                                           fillColor = "#f8766d",
                                                                           fillOpacity = 0.9,
                                                                           highlightOptions = highlightOptions(color = "white",
                                                                                                               weight = 1,
                                                                                                               bringToFront = TRUE),
                                                                           labelOptions = labelOptions(style = list("font-weight" = "normal",
                                                                                                                    padding = "3px 8px"),
                                                                                                       textsize = "10px",
                                                                                                       direction = "auto"))}
                                      else{print("Term appears in all plans.")}
                                      }
                                      print("search for things complete")}})

  observeEvent(input$clear_map, {print("clear map button clicked"); 
                                
                                 removeUI(selector = "#search_result_header")
                                 output$search_result_table <- DT::renderDataTable(data.frame())
                                
                                 leafletProxy("mymap", session) %>%  
                                 addPolygons(data = city_sf_final, 
                                             layerId = ~NAME,
                                             label = ~NAME,
                                             color = "#444444",
                                             opacity = 1.0,
                                             weight = 0.5,
                                             smoothFactor = 1.5,
                                             fillColor = "#f8766d",
                                             fillOpacity = 0.9,
                                             highlightOptions = highlightOptions(color = "white",
                                                                                 weight = 1,
                                                                                 bringToFront = TRUE), 
                                             labelOptions = labelOptions(style = list("font-weight" = "normal",
                                                                                       padding = "3px 8px"),
                                                                         textsize = "10px",
                                                                         direction = "auto"))})
  
  #update the location on map clicks
  observeEvent(input$mymap_shape_click, {city_id <- input$mymap_shape_click$id 
                                         city_row <- subset(city_sf_final, 
                                                            city_sf_final$NAME == city_id)
                                         search_string <- tolower(input$search)
                                         city_general_plan_href <- paste0("<a href='",
                                                                          city_row$filepath,
                                                                          "' target='_blank'>Link to General Plan</a>")
                                         output$city_selected <- renderUI({HTML('<hr/><h2>',
                                                                                input$mymap_shape_click$id,
                                                                                '</h2>', 
                                                                                city_general_plan_href)})
                                         print(paste("city row filepath:",
                                                     city_row$filepath))})
  
  
}
