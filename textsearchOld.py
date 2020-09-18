import os
import sys
from flask import Flask, request, render_template, redirect
from PyPDF2 import PdfFileMerger, PdfFileReader
import time
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
            
            with open(os.path.join("static/maps","coordinates.txt"), 'r',errors='ignore') as d:
                for line in d:
                    if freshword[0] in line:
                        divided=line.split("\t")
                        collectionla[i] =divided[1]
                        collectionlo[i]=divided[2].rstrip("\n")

            with open(os.path.join("static/data/cities",filename), 'r',errors='ignore') as f:
                collectiond [i]=f.readlines()
                i=i+1
            f.close() 


    
    return render_template('index.html')





def text_computing(s,e,wordcount,word,occurences,wordlist):

    resnm=[" "]* filecount
    resla=[" "]* filecount
    reslo=[" "]* filecount
    resy=[" "]* filecount
    fir=""
    las=""
    rescount=0
    wordw_occur = [""]* filecount
    prevfilenm=""
    ccountp=0
    icountp=0
    doesitcontainc=0
    doesitcontaini=0
    flag=0
    htmlc=""
    htmli=""
    htmlmap=""
    citycount=0
    citylist =[""]* filecount
    evercomputing=0

    var=0
    
    
    for i in range(s,e):
        
        htmlc +="<tr>"
        htmli +="<tr>"
        
        
        #print(collectionn[i])
        for line in collectiond[i]:      

            line=line.lower()
            
            
            for j in range(wordcount):
                if word[j] in line:
                    occurences[j]=occurences[j]+1
                    global ever
                    ever=1
                    evercomputing=1
                    if collectiontyp[i]== "c":
                        doesitcontainc=1
                    if collectiontyp[i]== "i":
                        doesitcontaini=1
                    
        for k in range(wordcount):        

            if doesitcontainc==1 or doesitcontaini==1 :
   
                
                if flag == 0:
                    
                    freshword=collectionn[i].strip('.txt')
                    pdfword=freshword+".pdf"
                    freshword=freshword.replace("-"," ")
                    if rescount==0:
                        repeatcheck=freshword.split("_")
                        fir=repeatcheck[0]
                    repeatcheck=freshword.split("_")
                    las=repeatcheck[0]
                    
                    if collectiontyp[i] == "c":
                        freshword=freshword.replace("City","")
                        
                    if collectiontyp[i] == "i":
                        
                        freshword=freshword.replace("county","")                   
                    freshword=freshword.split("_")
            
                    resnm[rescount]=freshword[0]
                   
                    resla[rescount]=collectionla[i]
                    reslo[rescount]=collectionlo[i]

                    rescount=rescount+1
                    if prevfilenm != freshword[0]:
                        citylist[citycount]=str(freshword[0])
                        citycount=citycount+1
                        if collectiontyp[i] == "c":
                            htmlc += "</table><table class='hoverTable' ><td rowspan='0' style='width:180px;'>"+str(freshword[0])+"</td>"
                            ccountp=ccountp+1
                        if collectiontyp[i] == "i":
                            htmli += "</table><table class='hoverTable' ><td rowspan='0' style='width:180px;'>"+str(freshword[0])+"</td>"
                            icountp=icountp+1
                        prevfilenm=freshword[0]
                    else:
                        htmlc += ""
                        htmli += ""
                    if collectiontyp[i] == "c":
                        htmlc += "<td style=width:180px>"+'<a href="/outp/'+pdfword+'/'+wordlist+'/'+str(wordcount)+'">'+str(freshword[1])+"</a>"+"</td>"
                    if collectiontyp[i] == "i":
                        htmli += "<td style=width:180px>"+'<a href="/outp/'+pdfword+'/'+wordlist+'/'+str(wordcount)+'">'+str(freshword[1])+"</a>"+"</td>"                    
                    wordw_occur[var]="<em style='color:green'><b>"+str(freshword[0])+"</b></em><br>"+'<a href="/outp/'+pdfword+'/'+wordlist+'/'+str(wordcount)+'">'+str(freshword[1])+"</a><br>"
                    flag=1
                    var=var+1
                    varcpy=var-1
                if collectiontyp[i] == "c":
                    htmlc += "<td style=width:180px>"+str(word[k])+"</td>"+"<td style=width:180px>"+str(occurences[k])+"</td>"
                if collectiontyp[i] == "i":
                    htmli += "<td style=width:180px>"+str(word[k])+"</td>"+"<td style=width:180px>"+str(occurences[k])+"</td>"
                wordw_occur[varcpy]+=str(word[k])+" : "+str(occurences[k])+"<b style='color:orange;'> times</b><br>"

        
         
        occurences = [0] * wordcount
        if doesitcontainc == 1:
          
            htmlc += "</tr>"
        else:
            htmlc = htmlc[:-4]
        if doesitcontaini ==1:
           
            htmli += "</tr>"
        else:
            htmli = htmli[:-4]
        flag=0
        doesitcontaini=0
        doesitcontainc=0


        
    mapobject = [[""] * 3 for i in range(citycount)]


    if evercomputing != 0:
        
        for i in range(citycount):
            flag=0
            mapobject[i][0]=resla[i]
            mapobject[i][1]=reslo[i]
            
            for j in range(rescount):
                
                if citylist[i] in wordw_occur[j]:
                    if flag == 1:
                        
                        combined="<em style='color:green'><b>"+citylist[i]+"</b></em><br>"
                        wordw_occur[j]=wordw_occur[j].replace(combined,"")

                    flag=1       
                    mapobject[i][2]+= wordw_occur[j]
                
            
            
        ############################ map marker definition ###############################################

        part=[{
                     'icon': {'url':'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'},
                     
                     'lat': mapobject[0][0],
                     'lng': mapobject[0][1],
                     'infobox': mapobject[0][2],
                     'animation': 'google.maps.Animation.DROP',
                        
                  },
                ]



        for i in range(citycount):


            part+=[{
                     'icon': {'url':'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'},
                
                     'lat':  mapobject[i][0],
                     'lng': mapobject[i][1],
                     'infobox': mapobject[i][2],
                     'animation': 'google.maps.Animation.DROP',
                        
                  },
                ]
    else:
        part=[]
    ############################ map marker definition ###############################################
    return htmlc, part,htmli,ccountp,icountp, resnm,fir,las


@app.route('/', methods=['POST'])
def my_form_post():
    #start = time.process_time()
    wordcount=1

    flag=0
    wordi=" "
    freshword=" "
    wordi=request.form['u']
    print(wordi)

    if "," in wordi:
        word=wordi.split(",")
        wordcount=len(word)
        for k in range(wordcount):
            word[k]=word[k].replace(',','')
            word[k]=word[k].strip(' ')
    else:
        wordcount=1
        word=[wordi]
        
    occurences = [0] * wordcount    
    
    html0=""
    htmli=""
  
    for i in range(wordcount):
        word[i]=word[i].lower()
    print(word)
    html0+= "<center>"
    html0 += "<table class='hoverTable'>"+"\n"
    html0 += "<th style=width:180px>"+"City"+"</th>"+"\n"
    html0 += "<th style=width:180px>"+"Year"+"</th>"+"\n"
    htmli+= "<center>"
    htmli += "<table class='hoverTable'>"+"\n"
    htmli += "<th style=width:180px>"+"County"+"</th>"+"\n"
    htmli += "<th style=width:180px>"+"Year"+"</th>"+"\n"
    for m in range(wordcount):
        htmli += "<th style=width:180px>"+"Key Phrase"+"</th>"+"\n"  
        htmli += "<th style=width:180px>"+"Occurences"+"</th>"+"\n"
        html0 += "<th style=width:180px>"+"Key Phrase"+"</th>"+"\n"  
        html0 += "<th style=width:180px>"+"Occurences"+"</th>"+"\n"
    html0 += "</tr>"+"\n"
    htmli += "</tr>"+"\n" 
    wordlist = ""
    for x in range(wordcount):
        if wordcount ==1:
            wordlist= word[0]
            break
        wordlist += word[x]+',' 
    wordlist= wordlist.strip(',')
  
    if __name__ == '__main__':
        
        with ThreadPoolExecutor() as executor:
            
            f1= executor.submit(text_computing,0,int(pstart),wordcount,word,occurences,wordlist)
            
            f2= executor.submit(text_computing,int(pstart),filecount,wordcount,word,occurences,wordlist)
            
            p1=f1.result()
            
            p2=f2.result()
            
    html0+=p1[0]+p2[0]
    htmli+=p1[2]+p2[2]
    ccountp=p1[3]+p2[3]
    icountp=p1[4]+p2[4]

    if p1[7] == p2[6]:

        if "City" in p1[7]:
            
            ccountp=ccountp-1
        if "county" in p1[7]:
            icountp=icountp-1
           

    
    lato=37.4419
  
    
    ########################## map declaration ######################################################
##    sndmap = Map(
##    identifier="sndmap",
##    lat=37.4419,
##    lng=-122.1419,
##    style='height:400px;width:600px;margin:0;',
##    markers= p1[1]+p2[1],
##    fit_markers_to_bounds = True
##    )
    ########################## map declaration ######################################################

    results = p1[5]
    print(p1[],flush=True)
    results[:] = [x for x in results if x != ' ']
    for i, res in enumerate(results):
        results[i] = res.strip()
        
    cities = gpd.read_file("static/data/ca-places-boundaries/cities.shp")[['NAME','NAMELSAD', 'geometry']]
    cities.columns = ['name', 'color', 'geometry']
    cities.color = "#FF4500"
    
    dropList = []
    cityNames = cities['name'].to_list()
    for ind in cities.index:
        val = cityNames[ind]
        if val not in results:
            dropList.append(ind) 
    cities = cities.drop(dropList, axis=0)
        
    counties = gpd.read_file("static/data/CA_Counties/CA_Counties_TIGER2016.shp")[['NAME', 'NAMELSAD', 'geometry']]
    counties.columns = ['color', 'name', 'geometry']
    counties.color = "white"
    
    # dropList = []
    # for ind in counties.index:
    #     val = counties['name'][ind]
    #     if val not in results:
    #         dropList.append(ind)  
    # counties = counties.drop(dropList, axis=0)
    
    combined = counties.append(cities)
    mergedJson = json.loads(combined.to_json())
    jsonCombined = json.dumps(mergedJson)
    geosource = GeoJSONDataSource(geojson = jsonCombined)
    
    
    size = 800
    TOOLS = "hover"
    p = figure(
        x_axis_location=None, y_axis_location=None,
        plot_width=size,
        plot_height=size,
        tools=TOOLS,
        tooltips=[
            ("Name", "@name")
        ])
    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"
    p.patches('xs','ys', source = geosource, fill_color='color')
    
    mapScript, mapDiv = components(p)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files
        
    
    ########################## Makena's map declaration ##########






    global ever
    if ever==0:
        return render_template('noresult.html')

    else:
        html0 += "</table></center>"
        ever=0
        html0 = Markup(html0)
        htmli = Markup(htmli)
        #print(time.process_time() - start)
        return render_template('results.html', html0=html0,htmli=htmli,ccountp=ccountp,tcountc=tcountc,tcounti=tcounti,icountp=icountp,mapScript=mapScript,mapDiv=mapDiv)


@app.route('/outp/<string:city>/<string:words>/<int:coun>')
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
    print(fht)
    
    return render_template('downloadf.html',fht=fht)
    
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
     



