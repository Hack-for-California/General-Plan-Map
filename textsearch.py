import os
from flask import Flask, request, render_template
from flask import flash, redirect, session, abort
from PyPDF2 import PdfFileMerger, PdfFileReader
import fitz
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap 
from flask import Markup
import pandas as pd
import requests
import shutil
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.plotting import figure
import geopandas as gpd
from bokeh.models import GeoJSONDataSource
import json
from bokeh.io import show, curdoc
from bokeh.models import LogColorMapper, ColumnDataSource, DataTable, DateFormatter, TableColumn, NumberFormatter, HTMLTemplateFormatter, Div
from bokeh.palettes import Viridis6 as palette
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties
from bokeh.layouts import column, widgetbox, layout, row
import shapefile
from bokeh.models.callbacks import CustomJS
from bokeh.io import output_file, show
from bokeh.models import TextInput, Button
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import show, output_file
import shapely.affinity
import es 


app = Flask(__name__)                                                                                                               #create flask object
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0                                                                                         #avoid storing cache
bootstrap = Bootstrap(app)                                                                                                          #create bootstrap object


@app.route('/')                                                                                                                     #declare flask page url
def my_form():                                                                                                                      #function for main index
    return render_template('index.html')                                                                                            #return index page


def getResults(wordinput):                                                                                                          
    
    # countyPopFile = open('static/data/countyPopulations.csv')
    # countyPops = {}
    # for line in countyPopFile:
    #     parts = line.split(',')
    #     countyPops[parts[0]] = parts[1]
    # countyPopFile.close()
    
    
    # cityPopFile = open('static/data/cityPopulations.csv')
    # cityPops = []
    # for line in cityPopFile:
    #     parts = line.split(',')
    #     temp = cityPop()
    #     temp.name=parts[0]
    #     temp.type = parts[1]
    #     temp.county = parts[2]
    #     temp.population = parts[3]
    #     cityPops.append(temp)
    
    
    # txtFilenames = []
    # for filename in os.listdir("static/data/places"):
    #     if filename.endswith(".txt"):

    #         txtFilenames.appyend(filename)
    results = []
    query = wordinput

    ids, _ = es.search_contains_phrase(query)
    result_props = es.map_index_to_vals(ids)
    for result_prop in result_props:
        result_prop = result_prop.copy()
        result_prop['query'] = query 
        new_result = Result(**result_prop)
        place_props = es.get_place_properties(new_result.is_city, new_result.place_name)
        if new_result.is_city:
            new_result.cityType = place_props[0]
            new_result.county = place_props[1]
            new_result.population = int(place_props[2])
        else:
            new_result.cityType = 'county'
            new_result.county = new_result.place_name
            new_result.population = int(place_props[0])

        #TODO: Do additional things here to make new_result work 
        results.append(new_result)

    
        
    # word = query.split(",")
    # wordcount = len(word)
    # for fName in txtFilenames:
    #     isMatch = False
    #     # file = open("static/data/places/" + fName, 'r',errors='ignore')
    #     # with open("static/data/places/" + fName, 'r',errors='ignore') as file:
    #     #     data = file.read().replace('\n', '')
    #     # data = data.lower()
    #     occurences = []
    #     if fName in filenames:
    #         isMatch = True
    #     for w in word:
    #         if isMatch:
    #             num = 1 
    #         else:
    #             num = 0 
    #         occurences.append(num)

    #     if isMatch:
    #         tempResult = Result(cityFile = fName, wordcount=wordcount)
    #         tempResult.type = fName.split('-')[0].split('_')[1]
    #         parts = fName.split('-')[1:]
    #         parts[-1] = parts[-1].split('.')[0]
    #         year = parts[-1].split('_')[1]
    #         parts[-1] = parts[-1].split('_')[0]
    #         name = ""
    #         for part in parts:
    #             name += part + " "
    #         name = name[:-1]
    #         tempResult.cityName = name
    #         tempResult.year = year
    #         tempResult.occurences = occurences
    #         if tempResult.type == 'county':
    #             tempResult.population = int(countyPops[tempResult.cityName])
    #         else:
    #             cityPopVal = [pop for pop in cityPops if pop.name == tempResult.cityName]
    #             if len(cityPopVal) != 0:

    #                 tempResult.population = int(cityPopVal[0].population)
    #                 tempResult.cityType = cityPopVal[0].type
    #                 tempResult.county = cityPopVal[0].county
    #         results.append(tempResult)
    # if len(results) > 0:
    #     for res in results:
    #         for item in res.occurences:
    #             item = float(item)
    #     results.sort(key=lambda x: x.totalOccurences, reverse=True)
    return results

class cityPop:
    
    def __init__(self, county, population, name, type):
        
        self.county = "na"
        self.population = "na"
        self.name = "na"
        self.type = "na"
    
class Result:
    
    def __init__(self, state, filename, is_city, place_name, plan_date, filetype,  query, county='na', population=0, city_type='na', wordcount=1, total_occuraces=1 ):
        # place properties 
        self.state = state
        self.filename = filename
        self.is_city = is_city
        self.place_name = place_name
        self.plan_date = plan_date
        self.filetype = filetype
        #search things 
        self.occurences = [0] * wordcount
        self.totalOccurences = total_occuraces
        
        # additional properties 
        self.county = county
        self.population = 0
        self.cityType = city_type

        self.pdf_filename = self.filename.split('.')[0] + '.pdf'
        self.year = '<p hidden>'+self.plan_date+'</p> <a href="outp/'+self.pdf_filename+'/'+query+'" target="_blank">'+self.plan_date+"</a>"


    @property
    def cityName(self):
        return self.place_name
    
    @property
    def type(self):
        if self.is_city:
            return 'City'
        else:
            return 'county'
    
       
@app.route('/', methods=['POST'])                                                                                                   #connect search form to html page
def index_search_box():                                                                                                             #function for accepting search input
    wordinput=" "                                                                                                                   #initialize string input for search
    wordinput=request.form['u']                                                                                                     #set name for search form
    results = getResults(wordinput)
    matched_city_names = []
    matched_county_names = []
    cityResults = []
    countyResults = []
    countyPops = {}
    cityPops = {}
    uniqueCities = 0
    uniqueCounties = 0
    for res in results:
        if res.is_city:
            cityResults.append(res)
            matched_city_names.append(res.place_name) 
            cityPops[res.place_name] = res.population
        else:
            countyResults.append(res)
            countyPops[res.place_name] = res.population
            matched_county_names.append(res.place_name) 


    if len(results) < 1:
        return render_template('noresult.html')
    
    #load in city shape files 
    cities = gpd.read_file("static/data/ca-places-boundaries/cities.shp")[['NAME','NAMELSAD', 'geometry']]
    cities.columns = ['name', 'color', 'geometry']
    cities.color = "#d47500"
    cities['line_color'] = '#dedede'
    numCities = len(cities.index)
    
    #load in county shape files 
    counties = gpd.read_file("static/data/CA_Counties/CA_Counties_TIGER2016.shp")[['NAME', 'NAMELSAD', 'geometry']]
    counties.columns = ['color', 'name', 'geometry']
    counties.color = "#00a4a6"
    counties['line_color'] = '#b3b3b3'
    numCounties = len(counties.index)

    # if there are no results then set these shapes to white 
    cityResultsName = [res.cityName for res in results]
    cityNames = cities['name'].to_list()
    for ind in cities.index:
        val = cityNames[ind]
        if val not in cityResultsName:
            cities.at[ind, 'color']='white'
    
    for ind in counties.index:
        #parse name for matching 
        parts = counties['name'][ind].split(' ')[0:-1]
        val = ""
        if len(parts) == 1:
            val = parts[0]
        else:
            for part in parts:
                val += part + ' '
            val = val[0:-1]
        #print(val, flush=True)
        if val not in matched_county_names: 
            counties.at[ind, 'color'] = 'white'
    
    combined = counties.append(cities)
    mergedJson = json.loads(combined.to_json())
    jsonCombined = json.dumps(mergedJson)
    geosource = GeoJSONDataSource(geojson = jsonCombined)
    
    TOOLS = ["hover", "pan", "wheel_zoom", "save"]
    p2 = figure(
        x_axis_location=None, y_axis_location=None,
        x_axis_type="mercator", y_axis_type="mercator",
        tools=TOOLS,
        tooltips=[("Name", "@name")]
        )
    p2.grid.grid_line_color = None
    p2.hover.point_policy = "follow_mouse"
    
    #make population map work better
    maxCountyPop = 1
    for county in countyResults:
        if county.population > maxCountyPop:
            maxCountyPop = county.population
    
    cartCounties = counties
    for ind, county in zip(cartCounties.index, countyResults):
        names = counties['name'][ind].split(' ')[0:-1]
        name = names[0]
        if len(names) > 1:
            for n in names[1:]:
                name += ' ' + n

        pop = county.population #countyPops[name] 
        geo = cartCounties['geometry'][ind]
        if maxCountyPop == 1:
            scale = 1
        else:
            scale = (pop/maxCountyPop )**(1/2)
        cartCounties['geometry'][ind] = shapely.affinity.scale(geo, scale, scale)

    
    maxCityPop = 1
    for city in cityResults:
        if float(city.population) > float(maxCityPop):
            maxCityPop = city.population
    cartCities = cities
    for ind, city in zip(cartCities.index, cityResults):
        geo = cartCities['geometry'][ind]
        if maxCityPop == 1:
            scale = 1
        else:
            scale = (city.population/maxCityPop)**(1/2)
        cartCities['geometry'][ind] = shapely.affinity.scale(geo,scale,scale)
     
    combined = cartCounties.append(cartCities)
    countyJson = json.loads(combined.to_json())
    jsonCounty=json.dumps(countyJson)
    p2GeoSource = GeoJSONDataSource(geojson=jsonCounty)
    p2.patches('xs','ys',source=p2GeoSource,fill_color='color', line_color='line_color')   
    
    size = 850
    TOOLS = ["hover", "pan", "wheel_zoom", "save"]
    p = figure( 
        x_axis_location=None, y_axis_location=None,
        tools=TOOLS,
        tooltips=[("Name", "@name")])
    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"
    p.patches('xs','ys', source = geosource, fill_color='color', line_color='line_color')
    

    cityData = dict(
        names=[res.cityName for res in cityResults],
        years=[res.year for res in cityResults],
        types=[res.cityType for res in cityResults],
        fNames=[res.pdf_filename for res in cityResults],
        populations = [res.population for res in cityResults],
        counties = [res.county for res in cityResults],
        )

    countyData = dict(
        names=[res.cityName for res in countyResults],
        years=[res.year for res in countyResults],
        types=[res.type for res in countyResults],
        fNames=[res.pdf_filename for res in countyResults],
        populations=[res.population for res in countyResults],
        )
    
    uniqueCities = len(set(cityData["names"]))
    uniqueCounties = len(set(countyData["names"]))
    occurences=[res.totalOccurences for res in results],
    numOccurences = len(results[0].occurences)
    
    
    citySource = ColumnDataSource(cityData)
    
    columns = [
            TableColumn(field="names", title="Name"),
            TableColumn(field="years", title="Year", formatter=HTMLTemplateFormatter()),
            TableColumn(field="populations", title="Population", formatter=NumberFormatter(format='0,0')),
            TableColumn(field="counties", title="County"),
        ]
    city_table = DataTable(source=citySource, columns=columns, width=size, height=600,reorderable=False, index_position=None)
    
    countySource = ColumnDataSource(countyData)
    
    columns = [
            TableColumn(field="names", title="Name"),
            TableColumn(field="years", title="Year", formatter=HTMLTemplateFormatter()),
            TableColumn(field="populations", title="Population", formatter=NumberFormatter(format='0,0')),
        ]
    county_table = DataTable(source=countySource, columns=columns, reorderable=False, index_position=None)
    
    cityTab = Panel(title="Cities", child=city_table)
    countyTab = Panel(title="Counties", child=county_table)
    tabs = Tabs(tabs=[cityTab, countyTab])

    resultsDiv = Div(text="""
                     <h1>{} out of {} cities have a match.</h1>
                     <h1>{} out of {} counties have a match.</h1>
                     """.format(uniqueCities, numCities, uniqueCounties, numCounties))
    
    popMap = Panel(title="Population", child=p2)
    outlineMap = Panel(title="Spatial", child=p)
    mapTabs = Tabs(tabs=[outlineMap, popMap])
    
    l = layout(column([row([mapTabs, resultsDiv]), tabs]))
    lScript,lDiv = components(l)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    return render_template('results.html',lScript=lScript,lDiv=lDiv)                                                                #render results page with map and table object as arguments



@app.route('/outp/<string:city>/<string:words>')                                                                                    #route for page containing highlighted pdf
def highlight_pdf(city, words):                                                                                                      #function for highlighting pdf phrases with pdf file name, list of words and phrase count as inputs

    complete_name = os.path.join("static/data/places", city)                                                                        #path for city pdf file
    doc = fitz.open(complete_name)                                                                                                  #create open pdf file object
    page_count= len(doc)                                                                                                            #find no. of pages in pdf               
    if "," in words:
        list_split=words.split(",")                                                                                                 #split wordlist by commas
    else:
        list_split=[words]                                                                                                          #if no commas means single word
    wordcount=len(list_split)
    text_instances = [" "] * wordcount                                                                                              #occurences of a phrase in a page
    for i in range(page_count):
        for k in range(wordcount):
            text_instances[k] = doc[i].searchFor(list_split[k],hit_max = 100)                                                            #search for the phrase in the page(maximum 100 occurences)
        for k in range(wordcount):      
            for inst in text_instances[k]:
                highlight = doc[i].addHighlightAnnot(inst)                                                                          #highlight all occurences of phrase
    highlighted_complete_name = os.path.join("static/data/pdfoutput","output.pdf")                                                  #path for highlighted pdf            
    doc.save(highlighted_complete_name)                                                                                             #save highlighted pdf
    doc.close()
    fht= 'window.location.href = "/static/data/pdfoutput/output.pdf";'                                                              #send highlighted pdf link
 
    fht = Markup(fht)                                                                                                               #make the link safe for sending to html
    
    return render_template('download.html',fht=fht)                                                                                 #render pdf file with the higlighted pdflink as argument
    

    
if __name__ == "__main__":                                                                                                          #run app on local host at port 5000 in debug mode
    
    app.run(host="0.0.0.0", port=5000, debug=True)
     



