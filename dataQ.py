## Master input Script for Data quarantine
## This functions handles input file, moves it through pipeline and outputs modified version & log file
## daniel.barto2@nm.state.us
## 01/09/2020

#call in command line (exactly!) like: python dataQ.py INPUTDATAfile.csv

import sys
import os
from clean import s_headers #custom function
from check import masterschool_compare #custom function
from logger import log

try:
    import pandas as pd
except:
    log.info("You are missing PANDAS dependencies, installing now....")
    os.system('pip install pandas')
try:
    import xlrd
except:
    log.info("You are missing XLRD dependencies, installing now....")
    os.system('pip install xlrd')

#Parse command line file
inputFILE = ((sys.argv [1]))

#Eval to see what file it is
# get the length of string
length = len(inputFILE)
dataFILEext = inputFILE[length - 4:]


if dataFILEext == ".csv":
    log.info('Reading in CSV File: %s :',inputFILE )
    dfFILE = pd.read_csv(inputFILE)
elif dataFILEext == ".sav":
    log.info('Reading in SPSS File: %s :',inputFILE )
    dfFILE = pd.read_spss(inputFILE, encoding = 'utf-8')
elif dataFILEext == "xlsx":
    log.info('Reading in Excel File: %s :',inputFILE )
    dfFILE = pd.read_excel(inputFILE, encoding = "ISO-8859-1")
elif len(sys.argv) > 2:  #Lazy eval here to detect spaces TODO will block multiple parmeters
    log.info('I Detected a space in filename')
    log.info('Please enclose file name in quotations')
    log.info('example: -->"student grades.csv"<---')
    log.info('Terminating now')
    exit()
else:
    log.info('Cannot read in unknown file type:  %s :', inputFILE)
    log.info('Files MUST be either .csv OR .sav OR .xlsx')
    log.info('Terminating now. Hope your day gets better')
    exit()


#Move the file into standarize heading routine
inputFILE_2=s_headers(dfFILE)


#Move the file into checks against our master dictornary
inputFILE_3=masterschool_compare(inputFILE_2)

#Make output file name
log.info('Writing File........')
finalFILEstr = 'dQ_'+inputFILE

#Write final dataframe to file with new filename
#ATTN: Be sure its the processed one you want.
inputFILE_3.to_csv(finalFILEstr)


#FUTURE GOALS
#Check District Code against District Name
#index against Master schools
#For students, compare DOB against grade (what if students fail)
#For schools, compare against grades applicable

log.info('Procedure Complete')