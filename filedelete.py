import sched, time
import os

while (1):
    #time.sleep(10)
    if len(os.listdir('static/data/pdfoutput') ) == 0:
        print("Directory is empty")
        continue
    else:
        one_minute_ago = time.time() - 60 
        folder = 'static/data/pdfoutput'
        os.chdir(folder)
        for somefile in os.listdir('.'):
            st=os.stat(somefile)
            mtime=st.st_mtime
            if mtime < one_minute_ago:
                os. remove(somefile)
