import os
from flask import Flask, request, render_template
from PyPDF2 import PdfFileMerger, PdfFileReader
import fitz

import pytesseract
from concurrent.futures import ThreadPoolExecutor
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from geopy.geocoders import Nominatim  
from flask import Markup
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pandas as pd
import requests
import shutil

from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.plotting import figure
import geopandas as gpd
from bokeh.models import GeoJSONDataSource
import json

app = Flask(__name__)
################### map configuration ##################################
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['GOOGLEMAPS_KEY'] = "AIzaSyC_vhsQmnw6oG5oX10gZugrJoUmwH-NgwI"
GoogleMaps(app, key="AIzaSyC_vhsQmnw6oG5oX10gZugrJoUmwH-NgwI")

################### map configuration ##################################
bootstrap = Bootstrap(app)

freshword=" "
filecount=0
pstart=0

collectionn = []
collectiond = []
collectionla = []
collectionlo = []
collectiontyp= []

tcountc=0
tcounti=0


i=0
fcount=0
ever=0

@app.route('/')
def my_form():

    
    global freshword
    freshword=" "
    global filecount
    filecount=0
    global pstart
    pstart=0

    global collectionn
    global collectiond
    global collectionla
    global collectionlo
    global collectiontyp
    global tcountc
    global tcounti
    tcountc=0
    tcounti=0
    i=0
    global fcount
    fcount=0
    global ever
    ever=0

    for filename in os.listdir("static/data/cities"):
        if filename.endswith(".txt"):
            
            filecount=filecount+1


    if filecount %2 ==0:
        pstart=filecount/2
    else:
        pstart=(filecount/2)+0.5


    collectionn = [" "]* filecount
    collectiond = [" "]* filecount
    collectionla = [" "]* filecount
    collectionlo = [" "]* filecount
    collectiontyp=[" "]*filecount
    



    splitterpc=""
    splitterpi=""


    for filename in sorted(os.listdir("static/data/cities")):
        if filename.endswith(".txt"):
            collectionn[i]=filename
        
            freshword=collectionn[i].strip('.txt')
            freshword=freshword.replace("-"," ")
            splitter=collectionn[i].split("_")

            
            if "City" in freshword:
                
                freshword=freshword.replace("City","")
                if splitter[0] != splitterpc:
                    splitterpc=splitter[0]
                    tcountc=tcountc+1
                collectiontyp[i]="c"
                
            if "county" in freshword:
                freshword=freshword.replace("county","")
                collectiontyp[i]="i"
                if splitter[0] != splitterpi:
                    splitterpi=splitter[0]
                    tcounti=tcounti+1

                
            freshword=freshword.split("_")
            
            

            with open(os.path.join("static/data/cities",filename), 'r',errors='ignore') as f:
                collectiond [i]=f.readlines()
                i=i+1
            f.close() 


    
    return render_template('index.html')


def getResults(wordi):
    countyPopFile = open('static/data/countyPopulations.csv')
    countyPops = {}
    for line in countyPopFile:
        parts = line.split(',')
        countyPops[parts[0]] = parts[1]
    countyPopFile.close()
    
    
    cityPopFile = open('static/data/cityPopulations.csv')
    cityPops = []
    for line in cityPopFile:
        parts = line.split(',')
        temp = cityPop()
        temp.name=parts[0]
        temp.type = parts[1]
        temp.county = parts[2]
        temp.population = parts[3]
        cityPops.append(temp)
    
    
    txtFilenames = []
    for filename in os.listdir("static/data/cities"):
        if filename.endswith(".txt"):
            txtFilenames.append(filename)
    results = []
    query = wordi
    word = query.split(",")
    wordcount = len(word)
    for fName in txtFilenames:
        isMatch = False
        file = open("static/data/cities/" + fName, 'r',errors='ignore')
        for line in file:         
                line=line.lower()
                for j in range(wordcount):
                    if word[j] in line:
                        if not isMatch:
                            isMatch = True
                            tempResult = result(cityFile = fName, wordcount=wordcount)
                            tempResult.type = fName.split('-')[0]
                            parts = fName.split('-')[1:]
                            parts[-1] = parts[-1].split('.')[0]
                            year = parts[-1].split('_')[1]
                            parts[-1] = parts[-1].split('_')[0]
                            name = ""
                            for part in parts:
                                name += part + " "
                            name = name[:-1]
                            tempResult.cityName = name
                            tempResult.year = year
                            if tempResult.type == 'county':
                                tempResult.population = int(countyPops[tempResult.cityName])
                            else:
                                cityPopVal = [pop for pop in cityPops if pop.name == tempResult.cityName]
                                if not len(cityPopVal) == 0:
                                    tempResult.population = int(cityPopVal[0].population)
                                    tempResult.cityType = cityPopVal[0].type
                                    tempResult.county = cityPopVal[0].county
                        tempResult.occurences[j] += 1
                        tempResult.totalOccurences += 1
        if isMatch:
            results.append(tempResult)
        file.close()
    if len(results) > 0:
        for res in results:
            for item in res.occurences:
                item = float(item)
        results.sort(key=lambda x: x.totalOccurences, reverse=True)
    return results, cityPops, countyPops

class cityPop:
    def __init__(self, name="na"):
        self.county = "na"
        self.population = "na"
        self.name = "na"
        self.type = "na"
    
class result:
    def __init__(self, cityFile="", wordcount=0):
        self.cityFile = cityFile
        self.occurences = [0] * wordcount
        self.totalOccurences = 0
        self.cityName = ""
        self.type = "city"
        self.year = "na"
        self.county = "na"
        self.population = "0"
        self.cityType = "na"
        
@app.route('/', methods=['POST'])
def my_form_post():
    #start = time.process_time()
    wordcount=1

    flag=0
    wordi=" "
    freshword=" "
    wordi=request.form['u']
    from bokeh.io import show, curdoc
    from bokeh.models import LogColorMapper, ColumnDataSource, DataTable, DateFormatter, TableColumn, NumberFormatter, HTMLTemplateFormatter, Div, Circle
    from bokeh.palettes import Viridis6 as palette
    from bokeh.plotting import figure
    from bokeh.sampledata.unemployment import data as unemployment
    from bokeh.sampledata.us_counties import data as counties
    from bokeh.layouts import column, widgetbox, layout, row
    import geopandas as gpd
    import shapefile
    from bokeh.models.callbacks import CustomJS
    from bokeh.io import output_file, show
    from bokeh.models import TextInput, Button
    from bokeh.models.widgets import Panel, Tabs
    import os
    import webbrowser
    from bokeh.io import show, output_file
    from bokeh.plotting import figure
    import geopandas as gpd
    from bokeh.models import GeoJSONDataSource
    import json
    import pandas as pd
    import shapely.affinity
    
    global txtFilenames 
    
    query = wordi
    word = query.split(",")
    results, cityPops, countyPops = getResults(wordi)
    cityResults = []
    countyResults = []
    uniqueCities = 0
    uniqueCounties = 0
    for res in results:
        res.cityFile = '/static/data/cities/' + res.cityFile.split('.')[0]+'.pdf'
        res.year = '<p hidden>'+res.year+'</p> <a href="'+res.cityFile+'" target="_blank">'+res.year+"</a>"
        if res.type == "county":
            countyResults.append(res)
        else:
            cityResults.append(res)
    if len(results) < 1:
        return render_template('noresult.html')
    
    cities = gpd.read_file("static/data/ca-places-boundaries/cities.shp")[['NAME','NAMELSAD', 'geometry']]
    cities.columns = ['name', 'color', 'geometry']
    cities.color = "#d47500"
    cities['line_color'] = '#dedede'
    numCities = len(cities.index)
    

    
    
    cityResultsName = [res.cityName for res in results]
    cityNames = cities['name'].to_list()
    for ind in cities.index:
        val = cityNames[ind]
        if val not in cityResultsName:
            cities.at[ind, 'color']='white'
    
    counties = gpd.read_file("static/data/CA_Counties/CA_Counties_TIGER2016.shp")[['NAME', 'NAMELSAD', 'geometry']]
    counties.columns = ['color', 'name', 'geometry']
    counties.color = "#00a4a6"
    counties['line_color'] = '#b3b3b3'
    numCounties = len(counties.index)
    
    for ind in counties.index:
        val = counties['name'][ind].split(' ')[0]
        flag = False
        for res in results:
            if res.type == 'county':
                if val == res.cityName:
                    flag = True
        if not flag:
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
    maxCountyPop = 0
    for county in countyResults:
        if county.population > maxCountyPop:
            maxCountyPop = county.population
    cartCounties = counties
    for ind in cartCounties.index:
        names = counties['name'][ind].split(' ')[0:-1]
        name = names[0]
        if len(names) > 1:
            for n in names[1:]:
                name += ' ' + n
        pop = float(countyPops[name])
        geo = cartCounties['geometry'][ind]
        scale = (pop/maxCountyPop )**(1/2)
        cartCounties['geometry'][ind] = shapely.affinity.scale(geo, scale, scale)

    
    maxCityPop = 0
    for city in cityResults:
        if city.population > maxCityPop:
            maxCityPop = city.population
    cartCities = cities
    for ind in cartCities.index:
        name = cities['name'][ind]
        pop = [r.population for r in cityPops if r.name == name]
        if len(pop) > 0:
            pop = float(pop[0])
        else:
            pop = 0.0
        geo = cartCities['geometry'][ind]
        scale = (pop/maxCityPop)**(1/2)
        cartCities['geometry'][ind] = shapely.affinity.scale(geo,scale,scale)
     
    combined = cartCounties.append(cartCities)
    countyJson = json.loads(combined.to_json())
    jsonCounty=json.dumps(countyJson)
    p2GeoSource = GeoJSONDataSource(geojson=jsonCounty)
    p2.patches('xs','ys',source=p2GeoSource,fill_color='color', line_color='line_color')   
    
    
    
    
    size = 850
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
        fNames=[res.cityFile for res in cityResults],
        populations = [res.population for res in cityResults],
        counties = [res.county for res in cityResults],
        )
    countyData = dict(
        names=[res.cityName for res in countyResults],
        years=[res.year for res in countyResults],
        types=[res.type for res in countyResults],
        fNames=[res.cityFile for res in countyResults],
        populations=[res.population for res in countyResults],
        )
    
    
    uniqueCities = len(set(cityData["names"]))
    uniqueCounties = len(set(countyData["names"]))
    occurences=[res.totalOccurences for res in results],
    numOccurences = len(results[0].occurences)
    
    for i,w in enumerate(word):
        cityOccurences = [cityres.occurences[i] for cityres in cityResults]
        cityData[w] = cityOccurences
        countyOccurences = [countyres.occurences[i] for countyres in countyResults]
        countyData[w] = countyOccurences
        
    
    citySource = ColumnDataSource(cityData)
    
    columns = [
            TableColumn(field="names", title="Name"),
            TableColumn(field="years", title="Year", formatter=HTMLTemplateFormatter()),
            TableColumn(field="populations", title="Population", formatter=NumberFormatter(format='0,0')),
            TableColumn(field="counties", title="County"),
        ]
    for w in word:
        columns.append(TableColumn(field=w, title=w,  formatter=NumberFormatter(format='0,0'))),
    city_table = DataTable(source=citySource, columns=columns, width=size, height=600,reorderable=False, index_position=None)
    # 
    countySource = ColumnDataSource(countyData)
    
    columns = [
            TableColumn(field="names", title="Name"),
            TableColumn(field="years", title="Year", formatter=HTMLTemplateFormatter()),
            TableColumn(field="populations", title="Population", formatter=NumberFormatter(format='0,0')),
        ]
    for w in word:
        columns.append(TableColumn(field=w, title=w,  formatter=NumberFormatter(format='0,0'))),
    county_table = DataTable(source=countySource, columns=columns, reorderable=False, index_position=None)
    
    popMap = Panel(title="Population", child=p2)
    outlineMap = Panel(title="Spatial", child=p)
    mapTabs = Tabs(tabs=[outlineMap, popMap])
    
    cityTab = Panel(title="Cities", child=city_table)
    countyTab = Panel(title="Counties", child=county_table)
    tabs = Tabs(tabs=[cityTab, countyTab])

    
    resultsDiv = Div(text="""
                     <h1>{} out of {} cities have a match.</h1>
                     <h1>{} out of {} counties have a match.</h1>
                     """.format(uniqueCities, numCities, uniqueCounties, numCounties))
    
    
    l = layout(column([row([mapTabs, resultsDiv]), tabs]))
    lScript,lDiv = components(l)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files





    return render_template('results.html',lScript=lScript,lDiv=lDiv)

@app.route('/outp/<string:ciopenPdfty>/<string:words>/<int:coun>')
def test_link(city,words,coun):


    
    cName = os.path.join("static/data/cities", city) 
    doc = fitz.open(cName)
    length= len(doc)
    if "," in words:
        text1=words.split(",")
    else:
        text1=[words]
    wordcount=len(text1)
    text_instances = [" "] * wordcount  
    for i in range(length):
        for k in range(wordcount):
            text_instances[k] = doc[i].searchFor(text1[k],hit_max = 100)

        for k in range(wordcount):      
            for inst in text_instances[k]:
                highlight = doc[i].addHighlightAnnot(inst)
    completeName = os.path.join("static/data/pdfoutput","output.pdf")            
    doc.save(completeName)
    doc.close()
    dd="lol"
    fht= 'window.location.href = "/static/data/pdfoutput/output.pdf";'
 
    fht = Markup(fht)
    
    return render_template('downloadf.html',fht=fht)
    
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
     



