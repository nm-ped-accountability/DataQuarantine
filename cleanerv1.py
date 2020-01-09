
import pandas as pd
import logging
import time


#Initalize Log changes
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Setup input paths
#file="\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\Student_Snapshot_Template_Extract_TEST-DNU.csv" #orgfile
file="\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\Student_Snapshot_Template_Extractsmallv2-DNU.csv" #debug
#Read in input file to csv
logger.info('Reading in File........')
dfFILE= pd.read_csv(file)


#Setup dict paths
msdictFILE_2020='\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2020.csv'
msdictFILE_2019='\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2019.csv'
msdictFILE_2018='\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2018.csv'
msdictFILE_2017='\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2017.csv'
#Note there are more previous years but just using these for quick debugs for now.

#Read in files to dicts
#NOTE The set_index(#) value is the column we want as keys In this case the schnumb is the unique id for each LEA.
ms_2020=pd.read_csv(msdictFILE_2020, encoding = "ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict() #Encoding parmeter to read in werid SPSS files
ms_2019=pd.read_csv(msdictFILE_2019, encoding = "ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict() #Encoding parmeter to read in werid SPSS files
ms_2018=pd.read_csv(msdictFILE_2018, encoding = "ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict() #Encoding parmeter to read in werid SPSS files
ms_2017=pd.read_csv(msdictFILE_2017, encoding = "ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict() #Encoding parmeter to read in werid SPSS files


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
        logger.info('School Number Heading Changed to schcode')
    if c in distCodeSET:
        dfFILE.rename(columns={c: "distnumb"}, inplace=True)
        logger.info('District Number Heading Changed to distcode')
    if c in schnameSET:
        dfFILE.rename(columns={c: "schname"}, inplace=True)
        logger.info('School Name Heading Changed to schname')
    if c in distnameSET:
        dfFILE.rename(columns={c: "distname"}, inplace=True)
        logger.info('District Name Heading Changed to distname')

#Fix capitalization issues for our string columns
dfFILE['schname']=dfFILE['schname'].str.title()
dfFILE['distname']=dfFILE['distname'].str.title()
#dfFILE['NamePLACEHOLDER']= dfFILE['NamePLACEHOLDER'].dropna() #might need this if null values

#Create Schnumb todo: check if one doesn't exists
dfFILE['schnumb'] = (dfFILE['distnumb']*1000) + dfFILE['schcode']


#Begin inputfile and Master Schools comparisions here
#TODO: Exterior loop to cycle through dicts if mismatch found on 2020

#Membership Evaluation
dfFILE['schnumbmatch']=dfFILE['schnumb'].isin(ms_2020['schcode'].keys())
dfFILE['schnamematch']=dfFILE['schname'].isin(ms_2020['schname'].values())

#Membership EVAL take 2
# Start by checking school name with school ID
fileSCHNAME = dfFILE['schname']
fileSCHNUMB = dfFILE['schnumb']

logger.info('Database Compare')
for i in fileSCHNUMB:
    try:
        print(ms_2020['schname'][i])
        dfFILE['ms_dict_name'] = ms_2020['schname'][i]
    except KeyError:
        logger.info("ATTENTION!!!!!!!!!!!!!!!!!! This key was not found in dict: %f", i)


time.sleep(1) #wait a sec for error check before writing file
logger.info('Writing File........')

dfFILE.to_csv('outvfull.csv')
#Check District Code against District Name

#index against Master schools

#For students, compare DOB against grade (what if students fail)

#For schools, compare against grades applicable

logger.info('Procedure Complete')
