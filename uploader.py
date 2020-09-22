from __future__ import print_function
import shutil,os
import sys
from flask import Flask, request, render_template, redirect,flash, session, abort, url_for,Markup
from flask_mail import Mail, Message
from PyPDF2 import PdfFileMerger, PdfFileReader
import fitz
import pytesseract
from werkzeug.utils import secure_filename
import requests
import subprocess
import ghostscript
import PyPDF2



app = Flask(__name__)                                                                                                                   #create flask object
mail= Mail(app)                                                                                                                         #create mail object
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0                                                                                             #to avoid storing cache

app.config['MAIL_SERVER']='smtp.gmail.com'                                                                                              #use gmail server
app.config['MAIL_PORT'] = 465                                                                                                           #set mail port
app.config['MAIL_USERNAME'] = 'generalplanserver@gmail.com'                                                                             #set sender email id
app.config['MAIL_PASSWORD'] = '@generalplan'                                                                                            #set sender password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)                                                                                                                        #build object again


@app.route('/')
def home():                                                                                                                             #function for log in screen
    del_list=""                                                                                                                         #list of files in delete section
    for filename in os.listdir("static/data/places"):
        if filename.endswith(".txt"):                                                                   
            filename=filename.replace(".txt","")
            del_list += '<option value="'+filename+'">'+filename+'</option>'                                                            #add each file name in selection list
    del_list=Markup(del_list)                                                                                                           #mark the html script as safe object
    if not session.get('logged_in'):                                                                                                    #if not logged in return login page
        return render_template('login.html')
    else:
        session['logged_in'] = False                                                        
        return render_template('upload_index.html',del_list=del_list)                                                                   #if logged in update file list



@app.route('/', methods=['POST'])
def do_admin_login():                                                                                                                   #function to collect username password
    if request.form['password'] == '@generalplan' and request.form['username'] == 'admin':                                                      #check username and password
        session['logged_in'] = True
    else:
        flash('Incorrect Username/Password')                                                                                            #if ID doesnt match username password                                                         
    return home()



@app.route('/delpg')
def delete_page_update():                                                                                                               #to update page list
    session['logged_in'] = True
    return redirect(url_for('home'))
    
@app.route('/delete', methods = ['POST'])                                                        
def delete_file():                                                                                                                      #function to delete file from list
    del_req=request.form['deleter']                                                                                                     #access delete button argument
    del_req=del_req+".pdf"
    rempdf = os.path.join("static/data/places", del_req)
    rempdftemp=rempdf.replace("places","temp")
    remtxt= rempdf.replace(".pdf",".txt")                                                           
    try:
        os.remove(remtxt)                                                                                                               #remove text file followed by pdf
    except:
        print("not found")
    try:
        os.remove(rempdf)                                                                                                              #remove text file followed by pdf
    except:
        print("not found")
    try:
        os.remove(rempdftemp)                                                                                                              #remove text file followed by pdf
    except:
        print("not found")
    
 
    return redirect(url_for('delete_page_update'))
    

            

@app.route('/upload', methods = ['GET', 'POST'])                                                                                        #route to upload form in upload_index html in for getting files and posting to the server
def upload_file1():                                                                                                                     #function to upload file
    
    if request.method == 'POST':                                                                                                        #when upload button is clicked
        
        files = request.files.getlist("file")                                                                                           #get list of files uploaded in form
        for file in files:                                                                                                              #open place pdf file
            print(file.filename)
            location_name=""
            if request.form['type'] == "City":
                location_name=request.form['City']
            else:
                location_name=request.form['county']
            file.filename=request.form['state']+"_"+request.form['type']+"_"+location_name+"_"+request.form['year']+".pdf"       #generate filename with select form data
            print(file.filename)
            msg = Message('General Plan file upload', sender = 'generalplanserver@gmail.com', recipients = ['ckbrinkley@ucdavis.edu'])   #send email for download notification
            msg.body = "Dear Admin,\nA file named "+file.filename+" has been uploaded to the server.\n\nGeneral Plan Server."
            mail.send(msg)                                                                                                              #send mail for file upload to server
            completeName = os.path.join("static/data/places",file.filename)

            print(completeName)
            tempname=os.path.join("static/data/temp",secure_filename(file.filename))                                                    #temporary copy file in case compression is not possible
            file.save(completeName)                                                                                                     #save file to server         
            arg1= '-sOutputFile='+ tempname                                                                                             #path for output file after compression to reduce pdf size
            p = subprocess.Popen(['/usr/bin/gs',
                                  '-sDEVICE=pdfwrite','-dCompatibilityLevel=1.4',
                                  '-dPDFSETTINGS=/screen','-dNOPAUSE', '-dBATCH',  '-dQUIET',
                                  str(arg1),completeName ], stdout=subprocess.PIPE)                                                     #function to compress pdf
            try:
                out, err = p.communicate(timeout=1800)                                                                                  #try compression for 1800s max
            except subprocess.TimeoutExpired:
                p.kill()                                                                                                                #kill the process since a timeout was triggered                                                                                                   
                out, error = p.communicate()                                                                                            #capture both standard output and standard error
            else:
                pass

            try:
                fh= open(tempname, "rb")
                check=PyPDF2.PdfFileReader(fh)                                                                                          #check if pdf is valid file
                fh.close()
            except:
                print("invalid PDF file")
                fh.close()
                os.remove(tempname)                                                                                                     #remove temp file if compressed pdf is corrupt and causes exception
            else:
                pass
                os.remove(completeName) 
                shutil.move(tempname,"static/data/places")                                                                              #move compressed tempfile to places directory is compressed file is valid
            fname =completeName
            fnamecpy=fname
            doc = fitz.open(fname)                                                                                                      #open pdf file object
            length=len(doc)                                                                                                             #find no. of pages
            imornot=0                                                                                                                   #flag variable to check if pdf contains scanned data or text
            for page in doc:
                if not page.getText():                                                                                                  #check check if pdf contains scanned data or text
                    imornot=imornot+1

            if imornot > int(length/2):                                                                                                 #if more than half pages of pdf are scanned convert to text pdf through OCR  
                fname=fname.replace('.pdf', '')                                     
                textfile = open(fname + ".txt", "a")                                                                                    #create text file with place name
                for page in doc:                                                                        
                    pix = page.getPixmap(alpha = False)                                                                                 #generate image file from page
                    pixn=os.path.join("static/data/places","page-%i.png" % page.number)     
                    pix.writePNG(pixn)                                                                                                  #save page image as png 
                    pdfn=os.path.join("static/data/places","page-"+str(page.number)+".pdf")
                    with open(pdfn, 'w+b') as f:
                        text = pytesseract.image_to_string(pixn)                                                                        #obtain text from image
                        textfile.write(text)                                                                                            #write text from the image to text file
                        pdf = pytesseract.image_to_pdf_or_hocr(pixn, extension='pdf')                                                   #convert image to pdf
                        f.write(pdf)                                                                                                    #create pdf for the page
                        os.remove(pixn)                                                                                                 #remove the image after pdf creation
                    f.close()
                textfile.close()

                mergedObject = PdfFileMerger()                                                                                          #create file merger object

                for fileNumber in range(page.number+1):                                                                                 #merge all page pdfs into a single pdf for the particlular place
                    pdfn=os.path.join("static/data/places",("page-"+str(fileNumber)+".pdf"))
                    mergedObject.append(PdfFileReader(pdfn, 'rb'))                                                                      #append page to place pdf
                    os.remove(pdfn)                                                                                                     #remove appended page pdf from server
                 
                mergedObject.write(fnamecpy)                                                                                            #save the complete place pdf to single file in server
                
                mergedObject.close()
            

            else:                                                                                                                       #if the pdf contains less than hald scanned pages
                imornot=0
                fname=fname.replace('.pdf', '')             
                textfile = open(fname + ".txt", "wb")                                                                                   #create text document to store text data
                for page in doc:
                        text = page.getText().encode("utf8")                                                                            #get text from pdf page
                        textfile.write(text)                                                                                            #write text to text file for the place 
                        textfile.write(bytes((12,)))
                textfile.close()
               
            doc.close()         
    up="Files Uploaded Successfully!"
    
    
    return render_template('upload_confirm.html',up=up)                                                                                 #render upload confirmation message page


if __name__ == "__main__":                                                                                                              #run app on local host at port 5001 in debug mode                                                                                      
    app.secret_key = os.urandom(12)                                                                                                     #random key for log in authentication
    app.run(host="0.0.0.0", port=5001, debug=True)                          
     



