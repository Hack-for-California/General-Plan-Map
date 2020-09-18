import os
import sys
from flask import Flask, request, render_template, redirect
from PyPDF2 import PdfFileMerger, PdfFileReader
import time
import fitz
import webbrowser
import pytesseract
from concurrent.futures import ThreadPoolExecutor
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim  
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template('upload_index.html')


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file1():
    
    if request.method == 'POST':
        
        lastname=""
        files = request.files.getlist("file")
        for file in files:
            completeName = os.path.join("static/data/cities",secure_filename(file.filename))      
            file.save(completeName)
            fname =completeName
            fnamecpy=fname
            doc = fitz.open(fname)
            length=len(doc)
            imornot=0
            for page in doc:
                if not page.getText():
                    imornot=imornot+1

            if imornot > int(length/2):
                #print("Conversion required")
                fname=fname.replace('.pdf', '')
                textfile = open(fname + ".txt", "a")
                for page in doc:  # iterate through the pages
                    pix = page.getPixmap(alpha = False)  # render page to an image

                    #pytesseract.image_to_string(pix)
                    pixn=os.path.join("static/data/cities","page-%i.png" % page.number)
                    pix.writePNG(pixn)  # store image as a PNG
                    pdfn=os.path.join("static/data/cities","page-"+str(page.number)+".pdf")
                    with open(pdfn, 'w+b') as f:
                        text = pytesseract.image_to_string(pixn)
                        textfile.write(text)  # write text of page
                        
                       
                        pdf = pytesseract.image_to_pdf_or_hocr(pixn, extension='pdf')
                        #print(pdf)
                        #doc[page]=pdf
                        
                        f.write(pdf) 
                        os.remove(pixn)
                    f.close()
                textfile.close()

                mergedObject = PdfFileMerger()
                 
                # I had 116 files in the folder that had to be merged into a single document
                # Loop through all of them and append their pages
                for fileNumber in range(page.number+1):
                    pdfn=os.path.join("static/data/cities",("page-"+str(fileNumber)+".pdf"))
                    mergedObject.append(PdfFileReader(pdfn, 'rb'))
                    os.remove(pdfn)
                 
                # Write all the files into a file which is named as shown below
                mergedObject.write(fnamecpy)
                mergedObject.close()
            

            else:
                imornot=0
                #print("Conversion not required")
                fname=fname.replace('.pdf', '')
                textfile = open(fname + ".txt", "wb")
                for page in doc:
                        text = page.getText().encode("utf8")
                        textfile.write(text)  # write text of page
                        textfile.write(bytes((12,)))
                textfile.close()
            doc.close()

    completeName = os.path.join("static/maps","coordinates.txt")
    fcount=0
    lastname=""
    file1 = open(completeName, "w")  # write mode 
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
            
            
            file1.write(freshword[0]+"\t"+str(loc['lat'])+"\t"+str(loc['lng'])+"\n")
    file1.close() 
            
            


            
    up="Files Uploaded Successfully!"
    
    return render_template('upload_confirm.html',up=up)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
     



