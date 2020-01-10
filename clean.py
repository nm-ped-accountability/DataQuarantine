#standardize_headers
#This is the first part of pipeline
#These functions standarize headers and assign float/string datatypes
#LAST Step: Add school number
#daniel.barto2@state.nm.us

import sys
import pandas
from logger import log


#Loops through columns of input file to find match in set
#IF matched, changes to set.
#NOTE: Sets are hardcoded; need to exact match or it won't catch
def s_headers(dfFILE):

    #Standardize headings
    schnumbSET  = ['School_Number', 'School Number', 'LocationID','School Number', 'Location_ID']
    distCodeSET = ['District Code', 'Disc_code','District','District Location', 'District_Code']
    schnameSET =  ['Full_Location_Name']
    distnameSET = ['District_Name']

    #Loop through headings and rewrite if they match entry in sets above
    #Note: Each set comparison is unique (i.e need to fit in the defined set
    for c in dfFILE.columns:
        if c in schnumbSET:
            dfFILE.rename(columns={c:"schcode"},inplace=True)
            log.info('School Number Heading Changed to schcode')
        if c in distCodeSET:
            dfFILE.rename(columns={c: "distnumb"}, inplace=True)
            log.info('District Number Heading Changed to distcode')
        if c in schnameSET:
            dfFILE.rename(columns={c: "schname"}, inplace=True)
            log.info('School Name Heading Changed to schname')
        if c in distnameSET:
            dfFILE.rename(columns={c: "distname"}, inplace=True)
            log.info('District Name Heading Changed to distname')

    #Fix capitalization issues for our string columns
    dfFILE['schname']=dfFILE['schname'].str.title()
    dfFILE['distname']=dfFILE['distname'].str.title()
    #dfFILE['NamePLACEHOLDER']= dfFILE['NamePLACEHOLDER'].dropna() #might need this if null values

    #Create Schnumb todo: check if one doesn't exists
    dfFILE['schnumb'] = (dfFILE['distnumb']*1000) + dfFILE['schcode']

    return dfFILE