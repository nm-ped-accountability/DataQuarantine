# This script checks input file against our master_schools file

import pandas as pd
import time
from logger import log

# Initalize Log changes
#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)

#debug for into file here
#dfFILE = '......csv'

def masterschool_compare(dfFILE):



    # Setup dict paths
    msdictFILE_2020 = '\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2020.csv'
    msdictFILE_2019 = '\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2019.csv'
    msdictFILE_2018 = '\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2018.csv'
    msdictFILE_2017 = '\\\\172.30.5.107\\Assessment and Accountability\\Accountability\\zDanZone\\MasterSchools_DICTS\\ms2017.csv'

    # NOTE The set_index(#) value is the column we want as keys In this case the schnumb is the unique id for each LEA.
    # TODO: handle errors if it cant find dictfile
    ms_2020 = pd.read_csv(msdictFILE_2020, encoding="ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict()
    ms_2019 = pd.read_csv(msdictFILE_2019, encoding="ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict()
    ms_2018 = pd.read_csv(msdictFILE_2018, encoding="ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict()
    ms_2017 = pd.read_csv(msdictFILE_2017, encoding="ISO-8859-1", header=0, dtype={0: str}).set_index('schnumb').squeeze().to_dict()

    #Begin inputfile and Master Schools comparisions here
    #TODO: Exterior loop to cycle through dicts if mismatch found on 2020

    #Membership Evaluation
    dfFILE['schnumbmatch']=dfFILE['schnumb'].isin(ms_2020['schcode'].keys())
    dfFILE['schnamematch']=dfFILE['schname'].isin(ms_2020['schname'].values())

    #Membership EVAL take 2
    # Start by checking school name with school ID
    fileSCHNAME = dfFILE['schname']
    fileSCHNUMB = dfFILE['schnumb']

    log.info('Database Compare')
    for i in fileSCHNUMB:
        try:
            #print(ms_2020['schname'][i])
            dfFILE['ms_dict_name'] = ms_2020['schname'][i]
        except KeyError:
            log.warning("ATTENTION!!!!!!!!!!!!!!!!!! This key was not found in dict: %f", i)


    time.sleep(1) #wait a sec for error check before returning file

    return dfFILE