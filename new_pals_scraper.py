import requests
import json
import pandas as pd
import numpy as np
import os
#import time  # If website limits number of records within short timeframe, could emulate X-waivers scraper for 5-min pause: time.sleep(300)

# make file paths work on both Windows and Mac
path = os.getcwd()
data_path = os.path.join(path, 'data', 'BupePrescribers_Phila-in-SAMHSA_2019Q4-2020Q2_528recs.csv')

# use list of 528 names
df = pd.read_csv(data_path, index_col=False)

# IN THE FUTURE USE FIRST, LAST AND MIDDLE NAMES FROM NPI

# fix a few names that use hyphens and special characters inconsistently across databases
df['lastname'] = df['lastname'].replace('Biniaurishvili-Elison', 'Biniaurishvili')
df['lastname'] = df['lastname'].replace('Baker-Evens', 'Baker Evens')

# URLs to query
url1 = 'https://www.pals.pa.gov/api/Search/SearchForPersonOrFacilty'  # sic ('Facilty' misspelled in actual URL)
url2 = "https://www.pals.pa.gov/api/SearchLoggedIn/GetPersonOrFacilityDetails"

# initialize empty dataframes to collect results
pals_providers = pd.DataFrame()
pals_licenses = pd.DataFrame()
noresult = []

# lookup providers by looping over df rows
# search first by  first + last
for i in df.index:

    # fill in search parameters
    data1 = {
            'County': None,
            'FirstName': df['firstname'][i],  # [_] PULL SERIES FROM df
            'IsFacility': 0,
            'LastName': df['lastname'][i],  # [_] PULL SERIES FROM df
            'LicenseNumber': "",  # [_] USE EMPTY STRING
            'OptPersonFacility': "Person",
            'PageNo': 1,
            'PersonId': None,
            # [_] EMPTY STRING probably preferable (catch exceptions)
            'State': ""
    }

    page1 = requests.post(url1, data1).json()

    # if results, append results to dataframe
    if (len(page1) > 0):
        pals_providers = pals_providers.append(pd.DataFrame.from_dict(page1), ignore_index=True)
    else:
        noresult.append((df['firstname'][i], df['lastname'][i], df['dea_num'][i]))


# limit to relevant professions 
# doing this after the query for now - is it possible to pass these to the API as an isin or OR statement?
irrelevant_professions = ['Real Estate Commission', 'Cosmetology', 'Vehicle Board', 'Engineers', 'Accountancy', 'Barber  Examiners', 'Certified Real Est. Appraisers', 'Architects', 'Veterinary Medicine', 'Funeral Directors', 'Crane Operators', 'Auctioneer Examiners', 'Massage Therapy', 'Landscape Architects', 'Dentistry', 'Speech', 'Optometry']

pals_providers = pals_providers[~pals_providers['ProfessionType'].str.strip().isin(irrelevant_professions)]


# HAVEN'T UPDATED ANYTHING AFTER THIS POINT YET

# get detailed license info for remaining results
# for j in pals_providers.index:
#     data2 = {
#                 'IsFacility': str(data1['IsFacility']),
#                 'LicenseId': page1[0]['LicenseId'],
#                 'LicenseNumber': page1[0]['LicenseNumber'],
#                 'PersonId': page1[0]['PersonId']
#                 }



# Separate 1st and 2nd loops

        #loop over each license in first page
        # for j in page1:
        #     # query 2nd API
        #     data2 = {
        #         'IsFacility': str(data1['IsFacility']),
        #         'LicenseId': page1[0]['LicenseId'],
        #         'LicenseNumber': page1[0]['LicenseNumber'],
        #         'PersonId': page1[0]['PersonId']
        #         }

        #     page2 = requests.post(url2, data2).text
        #     page2 = json.loads(page2)
        #     # this produces a dictionary that contains lists. It seems that only 'PinItemList' contains info that is not included elsewhere. Extract that and remove the lists.

        #     # extract pin entry corresponding to license j and add to main dict
        #     if (len(page2)['PinItemList'] > 0):
        #         pin = page2['PinItemList'][0]
        #         page2.update(pin)

            # the disciplinary records seem to be in random order and key info is in PDFs, so for now I will just flag the people with a record
            # if (len(page2['DisciplinaryActionDetails']) > 0):
            #     page2.update({'DisciplinaryAction': 'Y'})
            # else:
            #     page2.update({'DisciplinaryAction': 'N'})

            # # remove lists from dict
            # rm_list = ['PinItemList', 'PrerequisiteInformation', 'OtherLicenseDetails', 'DisciplinaryActionDetails', 'StatusHistoryList', 'LicenseCSRInformation']

            # for key in rm_list:
            #     del page2[key]

            # # append to license datafrmae
            # pals_licenses = pals_licenses.append(pd.DataFrame([page2]))