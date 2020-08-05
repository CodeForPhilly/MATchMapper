# from os import pathconf_names
from numpy.core.numeric import NaN
import requests
import json
import pandas as pd
import os
#import time  # I haven't had any issues with timeouts

# make file paths work on both Windows and Mac
path = os.getcwd()
data_path = os.path.join(path, 'data', 'new_final_hfp_npi.csv')

# use list of 526 names from NPI results (2 missing from NPI)
df = pd.read_csv(data_path, index_col=False)

# create dicts of name corrections - changes NPI to match PALS
last_names_corrected = {
    'BAKER-EVENS': 'BAKER EVENS',
    'COLON RIVERA': 'COLON-RIVERA',
    'DE ROOS': 'DEROOS',
    'LA JOIE': 'LAJOIE',
    'LEVITT-GOPIE': 'GOPIE',
    'OHARA': "O'HARA",
    'STOBART-GALLAGHER': 'STOBART GALLAGHER',
    'KHATRI': 'KHATRI-CHHETRI',
    "O'BRIEN": 'OBRIEN'
}

first_names_corrected = {
    'STACY-ANN': 'STACY ANN'
}

# update NPI input data with corrected names
df = df.replace({'last_name': last_names_corrected})
df = df.replace({'first_name': first_names_corrected})

# and a few more idiosyncratic corrections
df['first_name'][df['last_name'] == 'JAGIELLO'] = 'BEN'
df['first_name'][df['last_name'] == 'BAURER'] = 'FREDERIC'
df['first_name'][df['last_name'] == 'MECHEM'] = 'CHARLES'


# URLs to query
url1 = 'https://www.pals.pa.gov/api/Search/SearchForPersonOrFacilty'  # sic ('Facilty' misspelled in actual URL)

# initialize empty dataframes to collect results
pals_providers = pd.DataFrame()
noresult = []

# lookup providers by looping over df rows
# by first + last name, then license no if no result
for i in df.index:
    print(i)
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

    # remove Profession ID since license has a "better" ID???
    # del page1['Profession ID']
    # if results, add to dataframe
    if (len(page1) > 0):
        pals_providers = pals_providers.append(pd.DataFrame(page1), ignore_index=True)
    else:
       noresult.append((df['first_name'][i], df['last_name'][i])) 

#pals_providers_backup = pals_providers

# FILTER INCORRECT RESULTS

# change dtype to INT64 so that they aren't changed to floats when merged w/ NPI which contains NaNs
pals_providers[['LicenseId', 'PersonId']] = pals_providers[['LicenseId', 'PersonId']].astype('Int64')

# recode empty strings to NaN
pals_providers = pals_providers.replace(r'^\s*$', NaN, regex = True)

# limit to relevant professions in license database - this should probably be checked occassionally in case they change the categories
relevant_professions = ['Medicine', 'Nursing', 'Osteopathic Medicine', 'Pharmacy', 'Radiology Personnel', 'Social Work', 'Physical Therapy', 'Occupational Therapy', 'Chiropractic', 'Psychology', 'Podiatry']

pals_providers = pals_providers[pals_providers['ProfessionType'].str.strip().isin(relevant_professions)]

# REMOVE NAMES THAT DO NOT APPEAR IN ORIGINAL NPI DATA

# Change one name that is listed multiple ways in PALS
pals_providers['LastName'][pals_providers['LastName'] == 'THOMAS-LESLIE'] = 'THOMAS'

# Use a merge to remove cases where the first and last name do not appear in NPI results (this may remove correct results if discrepancies haven't been resolved)
npi = df[['first_name', 'last_name', 'npi', 'middle_name']]
npi = npi.rename(columns = {'first_name': 'FirstName', 'last_name': 'LastName', 'middle_name': 'npi_middle'})

pals_providers = pd.merge(pals_providers, npi, how = 'right', on = ['FirstName', 'LastName'])

# remove cases with missing PersonId (no match in PALS)
pals_providers = pals_providers[~pals_providers['PersonId'].isna()]

# If there are multiple PersonIds associated with a name, try filtering on middle initial
pals_providers['person_ids'] = pals_providers.groupby(['FirstName', 'LastName'])['PersonId'].transform(lambda x: x.nunique())

pals_providers['drop'] = pd.Series()

for i in pals_providers.index:
    if pals_providers['person_ids'][i] > 1:
        if pals_providers['MiddleName'][i] is not NaN and pals_providers['npi_middle'][i] is not NaN:
            if pals_providers['MiddleName'][i][0] != pals_providers['npi_middle'][i][0]:
                pals_providers['drop'][i] = 1

pals_providers = pals_providers.drop(pals_providers[pals_providers['drop'] == 1].index)

# recalculate ids per name and flag names with multiple ids
pals_providers['person_ids'] = pals_providers.groupby(['FirstName', 'LastName'])['PersonId'].transform(lambda x: x.nunique())

pals_providers['PotentialFalsePos'] = pals_providers['person_ids'].apply(lambda x: 1 if x > 1 else 0)

# remove inactive licenses if the person has at least one active license
pals_providers['active_count'] = pals_providers.groupby(['FirstName', 'LastName'])['Status'].transform(lambda x: (x == 'Active').sum())

pals_providers = pals_providers[((pals_providers['Status'] != 'Inactive') & (pals_providers['Status'] != 'Expired')) | (pals_providers['active_count'] == 0)]

# drop columns used for filtering or duplicated in 2nd API
pals_providers = pals_providers.drop(columns=['active_count', 'drop', 'person_ids', 'DisciplinaryAction', 'DisciplinaryActionTypeId'])

pals_providers = pals_providers.reset_index(drop=True, inplace=True)


# 2ND API
pals_licenses = pd.DataFrame()
url2 = "https://www.pals.pa.gov/api/SearchLoggedIn/GetPersonOrFacilityDetails"


# get detailed license info for remaining results
for j in pals_providers.index:
    print(j)
    data2 = {
                'IsFacility': 0,
                'LicenseId': pals_providers['LicenseId'][j],
                'LicenseNumber': pals_providers['LicenseNumber'][j],
                'PersonId': pals_providers['PersonId'][j]
                }

    page2 = requests.post(url2, data2).text
    page2 = json.loads(page2)

    # extract pin entry corresponding to license j and add to main dict
    # if (len(page2['PinItemList']) > 0):
    #     pin = page2['PinItemList'][0]
    #     page2.update(pin)

    # the disciplinary records seem to be in random order and key info is in PDFs, so for now just flag the people with a record
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


# MERGE OUTPUTS
pals_licenses = pals_licenses[['LicenseTypeInstructions', 'RelationshipLicenseInstructions', 'obtainedBy', 'SpecialityType', 'StatusEffectivedate', 'IssueDate', 'ExpiryDate', 'LastRenewalDate', 'NextRenewal', 'Relationship', 'AssociationDate', 'ShowFullAddress', 'ProfessionId', 'IsActiveLink', 'DisciplinaryAction']]

pals_licenses.reset_index(drop=True, inplace=True)
pals_providers.reset_index(drop=True, inplace=True)

final_df = pals_providers.merge(pals_licenses, how='outer', left_index=True, right_index=True)

final_df.to_csv(os.path.join(path, 'data', 'pals_final.csv'), index=False)
