from geopy.geocoders import Nominatim  
from flask import Markup
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import requests
import os,sys

fcount=0
lastname=""
for filename in sorted(os.listdir("static/data/cities")):
    if filename.endswith(".txt"):
        freshword=filename.strip('.txt')
        freshword=freshword.replace("-"," ")
        freshword=freshword.replace("City","")
        freshword=freshword.split("_")
        if lastname== freshword[0]:
            continue
        lastname=freshword[0]
        location='https://maps.googleapis.com/maps/api/geocode/json?address='+freshword[0]+',CA&key=AIzaSyC_vhsQmnw6oG5oX10gZugrJoUmwH-NgwI'
        fcount=fcount+1
        response = requests.get(location)
        

        resp_json_payload = response.json()
        #print(resp_json_payload)
        loc=resp_json_payload['results'][0]['geometry']['location']
        completeName = os.path.join("static/maps","coordinates.txt")
        file1 = open(completeName, "w")  # append mode 
        file1.write(freshword[0]+"\t"+str(loc['lat'])+"\t"+str(loc['lng'])+"\n")
        file1.close() 
        #print(freshword,loc['lat'], loc['lng'],fcount)
        

                

