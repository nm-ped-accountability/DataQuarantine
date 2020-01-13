# This script checks input file against our master_schools file

import pandas as pd
import time
from logger import log

#debug for into file here
#dfFILE = '......csv'

def masterschool_compare(dfFILE, logVECTOR):

    # get school numbers
    fileSCHNUMB = dfFILE['schnumb']

    #yearMS = {'2020', '2019', '2018', '2017'}
    yearMS ={'2020'} #debug

    #get length of cols on df
    count_col = dfFILE.shape[1]  # gives number of col count

    #check to see if schname and schnumber present
    #logVECTOR = [snumb, dcode, schname, disname, stid, dob]
    if logVECTOR[0]==1 & logVECTOR[1]==1:
        #Main loop to go through years
        for y in yearMS:
            #Generate master school dictonrary
            msDICT = setup_dicts(y) #random order TODO: force yearly descending order
            #School number in MS compared to Dataset and School Name Comparison
            log.info('Dataset Compare to ms%s',yearMS)
            index = 0
            for i in fileSCHNUMB:
                fileKEY = ((dfFILE['schnumb'][index]))
                if (fileKEY in (msDICT['schcode'].keys())):
                        #School name Comparison
                        dfFILE.at[index,count_col+1]=dfFILE['schname'][index] #Print out dataframe name for ease
                        dfFILE.at[index,count_col+2]=msDICT['schname'][i] #Print out mastersschool name for ease
                        dfFILE.at[index,count_col+3]=fuzz_check(dfFILE['schname'][index], msDICT['schname'][i]) #compare
                else:
                    log.warning("ATTENTION!!!!!!!!!!!!!!!!!! This key was not found in dict: %f", i)
                index = index + 1

            # Membership Evaluation
     #       dfFILE['schnumbmatch'] = dfFILE['schnumb'].isin(ms_2020['schcode'].keys())
     #       dfFILE['schnamematch'] = dfFILE['schname'].isin(ms_2020['schname'].values())

        #set columns names
        dfFILE.rename(columns={count_col+1: "DF_Entry", count_col+2: "MS2020_Entry", count_col+3:"DF-MS_MATCH"},inplace=True)

    time.sleep(1) #wait a sec for error check before returning file
    return dfFILE


def fuzz_check(inptFILE, msFILE):
    chk = (inptFILE == msFILE)
    #log.info('Entered Fuzz check')
    return chk

def setup_dicts(year):
    # Setup dict paths
    if year=='2020':
        msdictFILE_2020 = '\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2020.csv'
        #msdictFILE_2020 = 'C:\\Users\\dan\\Desktop\\12_02_2019_ppe_to_dash\\Master Schools 2020 V1.csv'
        ms_2020 = pd.read_csv(msdictFILE_2020, encoding="ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict()
        return ms_2020
    if year=='2019':
        msdictFILE_2019 = '\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2019.csv'
        #msdictFILE_2019 = 'C:\\Users\\dan\\Desktop\\12_02_2019_ppe_to_dash\\Master Schools 2020 V1small.csv'
        ms_2019 = pd.read_csv(msdictFILE_2019, encoding="ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict()
        return ms_2019
    if year=='2018':
        msdictFILE_2018 = '\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2018.csv'
        #msdictFILE_2018 = 'C:\\Users\\dan\\Desktop\\12_02_2019_ppe_to_dash\\Master Schools 2020 V1small.csv'
        ms_2018 = pd.read_csv(msdictFILE_2018, encoding="ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict()
        return ms_2018
    if year=='2017':
        msdictFILE_2017 = '\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2017.csv'
        #msdictFILE_2017 = 'C:\\Users\\dan\\Desktop\\12_02_2019_ppe_to_dash\\Master Schools 2020 V1small.csv'
        ms_2017 = pd.read_csv(msdictFILE_2017, encoding="ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict()
        return ms_2017