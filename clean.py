#standardize_headers
#This is the first part of pipeline
#These functions standarize headers and assign float/string datatypes
#LAST Step: Add school number
#daniel.barto2@state.nm.us

import sys
import pandas as pd
from logger import log

#debug
try:
    import pandas as pd
except:
    log.info("You are missing PANDAS dependencies, installing now....")
    os.system('pip install pandas')

#Clean main function
def s_headers(dfFILE):

    #Standardize headings
    #Note: Each set comparison is unique (i.e need to exact fit in the defined set. Add entries with "example",)
    schnumbSET  = ['School_Number', 'School Number', 'LocationID','School Number', 'Location_ID','TestingSchoolCode']
    distCodeSET = ['District Code', 'Disc_code','District','District Location', 'District_Code', 'TestingDistrictCode']
    schnameSET =  ['Full_Location_Name', 'TestingSchoolName']
    distnameSET = ['District_Name', 'TestingDistrictName']
    stidSET = ['Student_ID', 'Student ID']
    dobSET = ['Date of Birth', 'Birthdate','Student_Birth_Date']


    #Construct logical Vector with columns we want. Add future columns in descending order.
    #Set null here add to vector below
    snumb=0 #School Number
    dcode=0 #District Number
    schname=0 #School Name
    disname=0 #District Name
    stid=0 #Student ID
    dob=0 #Date of birth

    #Loop through headings and rewrite if they match entry in sets above
    for c in dfFILE.columns:
        if c in schnumbSET or c == "schcode":
            dfFILE.rename(columns={c:"schcode"},inplace=True)
            log.info('School Number Heading Changed to schcode')
            snumb=1
        if c in distCodeSET or c == "distnumb":
            dfFILE.rename(columns={c: "distnumb"}, inplace=True)
            log.info('District Number Heading Changed to distcode')
            dcode=1
        if c in schnameSET or c == "schname":
            dfFILE.rename(columns={c: "schname"}, inplace=True)
            log.info('School Name Heading Changed to schname')
            schname=1
        if c in distnameSET or c == "distname":
            dfFILE.rename(columns={c: "distname"}, inplace=True)
            log.info('District Name Heading Changed to distname')
            disname=1
        if c in stidSET or c == "stid":
            dfFILE.rename(columns={c: "stid"}, inplace=True)
            log.info('Student ID Heading Changed to stid')
            stid=1
        if c in dobSET or c == "dob":
            dfFILE.rename(columns={c: "dob"}, inplace=True)
            log.info('Birthday Heading Changed to dob')
            dob=1
    #this order will be important
    logVECTOR = [snumb, dcode, schname, disname, stid, dob]

    #terminating if no recognized columns present
    col_check(logVECTOR)

    #Make Values Capital Letter
    make_capital(dfFILE, logVECTOR)

    #Create Schnumb
    schnumb_gen(dfFILE, logVECTOR)

    #Force datatype and length
    force_datatype(dfFILE, logVECTOR)

    #Check for duplicates in schools and/or students
    check_duplicates(dfFILE, logVECTOR)

    return dfFILE, logVECTOR

def col_check(logVECTOR):
    if sum(logVECTOR) == 0:
        log.info("Did not recognize any column names")
        log.info("Please edit names to match entries in my memory sets")
        log.info("Terminating now")
        exit()

def check_duplicates(dfFILE, logVECTOR):
    #note this performed in order
    if logVECTOR[4]==1:
        dupesWRITES=dfFILE.loc[dfFILE['stid'].duplicated(), :]
        log.info("Duplicates Found in stid, First record kept. See log for more info")
        dupesWRITES.to_csv('duplicatesDeleted.csv')

    #conflict between school code/ schnumb need to sort out
   # if logVECTOR[0]==1: #Check off the school code
   #     dupesWRITES=dfFILE.loc[dfFILE['schcode'].duplicated(), :]
   #     log.info("Duplicates Found")
   #     log.info(dupesWRITES)



def schnumb_gen(dfFILE, logVECTOR):
    if logVECTOR[0]==1 & logVECTOR[1]==1:
        dfFILE['schnumb'] = (dfFILE['distnumb']*1000) + dfFILE['schcode']
        log.info("Generated New Schunumb")

def force_datatype(dfFILE, logVECTOR):
    if logVECTOR[0]==1:
        dfFILE["schnumb"] = pd.to_numeric(dfFILE["schnumb"], errors='coerce')
    if logVECTOR[1]==1:
        dfFILE["distnumb"] = pd.to_numeric(dfFILE["distnumb"], errors='coerce')
    if logVECTOR[5]==1:
        dfFILE['dob'] = pd.to_datetime(dfFILE['dob'], errors='coerce').dt.date

def make_capital(dfFILE, logVECTOR):
    if logVECTOR[2]==1:
        dfFILE['schname']=dfFILE['schname'].str.title()
    if logVECTOR[3]==1:
        dfFILE['distname']=dfFILE['distname'].str.title()
    #dfFILE['NamePLACEHOLDER']= dfFILE['NamePLACEHOLDER'].dropna() #might need this if null values
