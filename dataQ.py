## Master input Script for Data quarantine
## This functions handles input file, moves it through pipeline and outputs modified version & log file
## daniel.barto2@nm.state.us
## 01/09/2020

#call in command line (exactly!) like: python dataQ.py INPUTDATAfile.csv

import sys
import os
from clean import s_headers #custom function
from check import masterschool_compare #custom function
from logger import log #custom function

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
try:
    import pyreadstat
except:
    log.info("You are missing .sav import dependencies, installing now....")
    os.system('pip install pyreadstat')
try:
    import xlsxwriter
except:
    log.info("You are missing .xlsx write dependencies, installing now....")
    os.system('pip install xlsxwriter')



#Parse command line file
inputFILE = ((sys.argv [1]))

#debug!!!
#inputFILE = "Student Snapshot Template Extractsmallv2.csv"

# get the length of string
length = len(inputFILE)
dataFILEext = inputFILE[length - 4:]

#Eval to see what file it is
if dataFILEext == ".csv":
    log.info('Reading in CSV File: %s :',inputFILE )
    dfFILE = pd.read_csv(inputFILE)
    ftype=".csv"
elif dataFILEext == ".sav":
    log.info('Reading in SPSS File: %s :',inputFILE )
    dfFILE = pd.read_spss(inputFILE)
    ftype=".sav"
elif dataFILEext == "xlsx":
    log.info('Reading in Excel File: %s :',inputFILE )
    dfFILE = pd.read_excel(inputFILE, encoding = "ISO-8859-1")
    ftype = ".xlsx"
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

log.info("Proceeding to Clean File")
#Move the file into standarize heading routine
[inputFILE_2, logVECTOR]=s_headers(dfFILE)

log.info("Proceeding to Check File")
#Move the file into checks against our master dictornary
inputFILE_3=masterschool_compare(inputFILE_2, logVECTOR)

#Last dataframe before write out be sure it is the one you want
finalFILE = inputFILE_3

#Make output file name
log.info('Writing File........')
finalFILEstr = os.getcwd()+'\\dQ_'+inputFILE

print(finalFILEstr)

#Output new modified file
if ftype ==".csv":
    finalFILE.to_csv(finalFILEstr)
elif ftype ==".sav":
    pyreadstat.write_sav(finalFILE, finalFILEstr)
elif ftype ==".xlsx":
    writer = pd.ExcelWriter(finalFILEstr, engine='xlsxwriter')
    finalFILE.to_excel(writer, sheet_name='Sheet1')
    writer.save()

#FUTURE GOALS
#Add student data read and prcoessing
#Student id handling
#add on minority or other demographic issues (?)

#For students, compare DOB against grade (what if students fail)
#For schools, compare against grades applicable

log.info('Procedure Complete')