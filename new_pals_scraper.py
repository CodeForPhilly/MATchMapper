from os import pathconf_names
from numpy.core.numeric import NaN
import requests
import json
import pandas as pd
import os
#import time  # I haven't had any issues with timeouts

# make file paths work on both Windows and Mac
path = os.getcwd()
data_path = os.path.join(path, 'data', 'new_final_hfp_npi.csv')

# use list of 528 names
df = pd.read_csv(data_path, index_col=False)

# there is probably a way to generalize these changes, but 
df['last_name'] = df['last_name'].replace('BAKER-EVENS', 'Baker Evens')
df['last_name'] = df['last_name'].replace('COLON RIVERA', 'Colon-Rivera')
df['last_name'] = df['last_name'].replace('DE ROOS', 'DeRoos')
df['last_name'] = df['last_name'].replace('LA JOIE', 'LaJoie')
df['last_name'] = df['last_name'].replace('LEVITT-GOPIE', 'Gopie')
df['last_name'] = df['last_name'].replace('OHARA', "O'Hara")
df['last_name'] = df['last_name'].replace('STOBART-GALLAGHER', 'Stobart Gallagher')
df['first_name'][df['last_name'] == 'JAGIELLO'] = 'Ben'
df['first_name'] = df['first_name'].replace('STACY-ANN', 'Stacy Ann')

# URLs to query
url1 = 'https://www.pals.pa.gov/api/Search/SearchForPersonOrFacilty'  # sic ('Facilty' misspelled in actual URL)

# initialize empty dataframes to collect results
pals_providers = pd.DataFrame()
noresult = []

# lookup providers by looping over df rows
# by first + last name, then license no if no result
for i in df.index:

    # fill in search parameters
    data1 = {
            'County': None,
            'IsFacility': 0,
            'FirstName': df['first_name'][i],
            #?'MiddleName': "'in': {}".format(middlenames), # change - won't retrieve result if they list initial in NPI and full name in PALS
            'LastName': df['last_name'][i],
            'LicenseNumber': "",
            'OptPersonFacility': "Person",
            'PageNo': 1,
            'PersonId': None,
            'State': ""
    }

    page1 = requests.post(url1, data1).json()

    # if results, add to dataframe
    if (len(page1) > 0):
        pals_providers = pals_providers.append(pd.DataFrame(page1), ignore_index=True)
    else:
       noresult.append((df['first_name'][i], df['last_name'][i])) 


# FILTER INCORRECT RESULTS

# recode empty strings to NaN
pals_providers = pals_providers.replace(r'^\s*$', NaN, regex = True)

# limit to relevant professions in license database - this should probably be checked occassionally in case they change the categories
relevant_professions = ['Medicine', 'Nursing', 'Osteopathic Medicine', 'Pharmacy', 'Radiology Personnel', 'Social Work', 'Physical Therapy', 'Occupational Therapy', 'Chiropractic', 'Psychology', 'Podiatry']

pals_providers = pals_providers[pals_providers['ProfessionType'].str.strip().isin(relevant_professions)]

# remove results that don't match on middle initial
names_orig = df.loc[:, ['first_name', 'middle_name', 'last_name']]
names_orig = names_orig.rename(columns = {'first_name': 'FirstName', 'last_name': 'LastName', 'middle_name': 'middle_name_npi'})

pals_providers = pd.merge(pals_providers, names_orig, on = ['FirstName', 'LastName'], how='left')

pals_providers.loc[(pals_providers['MiddleName'].notnull()) & (pals_providers['middle_name_npi'].notnull()) & (pals_providers['MiddleName'].str[0] != pals_providers['middle_name_npi'].str[0]), 'drop'] = 1

pals_providers = pals_providers.drop(pals_providers[pals_providers['drop'] == 1].index)

# drop columns used for filtering
pals_providers = pals_providers.drop(columns=['drop'])


# 2nd API
pals_licenses = pd.DataFrame()
url2 = "https://www.pals.pa.gov/api/SearchLoggedIn/GetPersonOrFacilityDetails"


# get detailed license info for remaining results
for j in pals_providers.index:
    data2 = {
                'IsFacility': pals_providers['IsFacility'][j],
                'LicenseId': pals_providers['LicenseId'][j],
                'LicenseNumber': pals_providers['LicenseNumber'][j],
                'PersonId': pals_providers['PersonId'][j]
                }

    page2 = requests.post(url2, data2).text
    page2 = json.loads(page2)

    # extract pin entry corresponding to license j and add to main dict
    if (len(page2['PinItemList']) > 0):
        pin = page2['PinItemList'][0]
        page2.update(pin)

    # the disciplinary records seem to be in random order and key info is in PDFs, so for now I will just flag the people with a record
    if (len(page2['DisciplinaryActionDetails']) > 0):
        page2.update({'DisciplinaryAction': 'Y'})
    else:
        page2.update({'DisciplinaryAction': 'N'})

    # remove lists from dict
    rm_list = ['PinItemList', 'PrerequisiteInformation', 'OtherLicenseDetails', 'DisciplinaryActionDetails', 'StatusHistoryList', 'LicenseCSRInformation']

    for key in rm_list:
        del page2[key]

    # append to license datafrmae
    pals_licenses = pals_licenses.append(pd.DataFrame([page2]))