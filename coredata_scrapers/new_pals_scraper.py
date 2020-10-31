from numpy.core.numeric import NaN
import requests
import json
import pandas as pd
import os
import re
import recordlinkage
from datetime import date

path = os.getcwd()
data_path = os.path.join(path, 'data', 'NPI_info_2020-08-03_526to528names_samtan_withALLaddresses.xlsx')
##TODO: Change input filename above to match whichever installment you're checking

df = pd.read_excel(data_path, index_col=False)

# function for toggling common name format discrepancies
def name_fixer(name):
    name = str(name)
    if " " in name:
        name = name.replace(" ", "-")
    elif "-" in name:
        name = name.replace("-", " ")
    elif "'" in name:
        name = name.replace("'", "")
    return name

# fix a few names that return incorrenct results when searching by license number
last_names_corrected = {
    'COLON RIVERA': 'COLON-RIVERA',
    'LEVITT-GOPIE': 'GOPIE',
    "O'BRIEN": 'OBRIEN'
}

df = df.replace({'last_name': last_names_corrected})

# list of relevant professions
professions = {
    'Medicine': 37,
    'Nursing': 43,
    'Osteopathic Medicine': 36
}

# 1st URL to query
# sic ('Facilty' misspelled in actual URL)
url1 = 'https://www.pals.pa.gov/api/Search/SearchForPersonOrFacilty'

# initialize empty dataframe to collect results
pals_providers = pd.DataFrame()
noresult = []

# loop over rows of NPI data
# for each name, loop over 3 relevant professions - the URL doesn't seem to accept multiple parameter values
for i in df.index:
    print("Name", (i + 1), "of", len(df.index))
    tmp = pd.DataFrame()
    for j in professions:
        data1 = {
            'County': None,
            'IsFacility': 0,
            'FirstName': df['first_name'][i],
            'LastName': df['last_name'][i],
            'ProfessionId': professions[j],
            'LicenseNumber': "",
            'OptPersonFacility': "Person",
            'PageNo': 1,
            'PersonId': None,
            'State': ""
        }

        page1 = requests.post(url1, data1).json()

        if len(page1) > 0:
                tmp = tmp.append(pd.DataFrame(page1), ignore_index=True)

        elif df['primary_taxonomy_license'][i] is not NaN:
            data1 = {
                'County': None,
                'IsFacility': 0,
                'FirstName': "",
                'LastName': "",
                'ProfessionId': professions[j],
                'LicenseNumber': df['primary_taxonomy_license'][i],
                'OptPersonFacility': "Person",
                'PageNo': 1,
                'PersonId': None,
                'State': ""
            }

            page1 = requests.post(url1, data1).json()

            if len(page1) > 0:
                tmp = tmp.append(pd.DataFrame(page1), ignore_index=True)

            else:
                data1 = {
                    'County': None,
                    'IsFacility': 0,
                    'FirstName': df['first_name'][i],
                    'LastName': df['last_name'][i],
                    'ProfessionId': "",
                    'LicenseNumber': "",
                    'OptPersonFacility': "Person",
                    'PageNo': 1,
                    'PersonId': None,
                    'State': ""
                }

                page1 = requests.post(url1, data1).json()

                if len(page1) > 0:
                    tmp = tmp.append(pd.DataFrame(page1), ignore_index=True)

                else:
                   last_alt = name_fixer(df['last_name'][i])

                   data1 = {
                       'County': None,
                       'IsFacility': 0,
                       'FirstName': df['first_name'][i],
                       'LastName': last_alt,
                       'ProfessionId': "",
                       'LicenseNumber': "",
                       'OptPersonFacility': "Person",
                       'PageNo': 1,
                       'PersonId': None,
                       'State': ""
                   }

                page1 = requests.post(url1, data1).json()

                if len(page1) > 0:
                    tmp = tmp.append(pd.DataFrame(page1), ignore_index=True)

        else:
            data1 = {
                    'County': None,
                    'IsFacility': 0,
                    'FirstName': df['first_name'][i],
                    'LastName': df['last_name'][i],
                    'ProfessionId': "",
                    'LicenseNumber': "",
                    'OptPersonFacility': "Person",
                    'PageNo': 1,
                    'PersonId': None,
                    'State': ""
                }

            page1 = requests.post(url1, data1).json()

            if len(page1) > 0:
                tmp = tmp.append(pd.DataFrame(page1), ignore_index=True)

            else:
                last_alt = name_fixer(df['last_name'][i])

                data1 = {
                    'County': None,
                    'IsFacility': 0,
                    'FirstName': df['first_name'][i],
                    'LastName': last_alt,
                    'ProfessionId': "",
                    'LicenseNumber': "",
                    'OptPersonFacility': "Person",
                    'PageNo': 1,
                    'PersonId': None,
                    'State': ""
                }

                page1 = requests.post(url1, data1).json()

                if len(page1) > 0:
                    tmp = tmp.append(pd.DataFrame(page1), ignore_index=True)

    if (len(tmp) > 0):
        pals_providers = pals_providers.append(tmp)
    else:
       noresult.append((df['first_name'][i], df['last_name'][i])) 


# drop duplicates
pals_providers = pals_providers.drop_duplicates()

# remove irrelevant professions
pals_providers = pals_providers[pals_providers['ProfessionType'].isin(professions.keys())]

pals_providers.reset_index(drop=True, inplace=True)

# USE FUZZY RECORD MATCH TO REMOVE FALSE POSITIVES

# first standardize phone number format
def phone_format(n):
    n = re.sub('[^0-9]','', n)
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1]

pals_providers['PhoneNo1'] = pals_providers['PhoneNo1'].apply(lambda x: NaN if not x else phone_format(x))

df['practice_loc1_phone'] = df['practice_loc1_phone'].str.replace(" ", "")
df['practice_loc2_phone'] = df['practice_loc2_phone'].str.replace(" ", "")
df['practice_loc3_phone'] = df['practice_loc3_phone'].str.replace(" ", "")
df['practice_loc4_phone'] = df['practice_loc4_phone'].str.replace(" ", "")
df['practice_loc5_phone'] = df['practice_loc5_phone'].str.replace(" ", "")
df['practice_loc6_phone'] = df['practice_loc6_phone'].str.replace(" ", "")
df['mail_loc_phone'] = df['mail_loc_phone'].str.replace(" ", "")

# limit to 5-digit zipcode
df['practice_loc1_zip'] = df['practice_loc1_zip'].str.slice(0,5)
df['practice_loc2_zip'] = df['practice_loc2_zip'].str.slice(0,5)
df['practice_loc3_zip'] = df['practice_loc3_zip'].str.slice(0,5)
df['practice_loc4_zip'] = df['practice_loc4_zip'].str.slice(0,5)
df['practice_loc5_zip'] = df['practice_loc5_zip'].str.slice(0,5)
df['practice_loc6_zip'] = df['practice_loc6_zip'].str.slice(0,5)
df['mail_loc_zip'] = df['mail_loc_zip'].str.slice(0, 5)

# use NPI credential field to create profession type
df['credential'] = df['credential'].str.replace('.', '')

df['ProfessionType'] = pd.Series()

for i in df.index:
    if df['credential'][i] is NaN:
        df['ProfessionType'][i] = NaN
    elif 'MD' in df['credential'][i]:
        df['ProfessionType'][i] = 'Medicine'
    elif ('DO' or 'D O') in df['credential'][i]:
        df['ProfessionType'][i] = 'Osteopathic Medicine'
    else:
        df['ProfessionType'][i] = 'Nursing'

# create full name column for comparison
df['full_name'] = pd.Series()

for i in df.index:
    if df['middle_name'][i] is NaN:
        df['full_name'][i] = df['first_name'][i] + " " + df['last_name'][i]
    else:
        df['full_name'][i] = df['first_name'][i] + " " + df['middle_name'][i] + " " + df['last_name'][i]

# create middle initial column
df['mid_init'] = df['middle_name'].str.slice(0, 1)
pals_providers['MidInit'] = pals_providers['MiddleName'].str.slice(0, 1)

# select pairs of rows to compare - we will compare every combination since the dataset is manageable in size
indexer = recordlinkage.Index()
indexer.full()
candidates = indexer.index(df, pals_providers)

# select columns for comparison
compare = recordlinkage.Compare()
compare.exact('ProfessionType', 'ProfessionType', label = 'ProfessionType')
compare.exact('primary_taxonomy_license', 'LicenseNumber', label = 'LicenseNumber')
compare.string('first_name', 'FirstName', threshold = 0.85, label = 'FirstName')
compare.string('other_names_first_name', 'FirstName', threshold = 0.85, label = 'FirstName_alt')
compare.string('middle_name', 'MiddleName', threshold = 0.85, label = 'MiddleName')
compare.exact('mid_init', 'MidInit', label = 'MidInit')
compare.string('last_name', 'LastName', threshold = 0.85, label = 'LastName')
compare.string('other_names_last_name', 'LastName', threshold = 0.85, label = 'LastName_alt')
compare.string('full_name', 'FullName', threshold = 0.85, label = 'FullName_match')
compare.exact('practice_loc1_zip', 'zipcode', label = 'zip1')
compare.exact('practice_loc2_zip', 'zipcode', label = 'zip2')
compare.exact('practice_loc3_zip', 'zipcode', label = 'zip3')
compare.exact('practice_loc4_zip', 'zipcode', label = 'zip4')
compare.exact('practice_loc5_zip', 'zipcode', label = 'zip5')
compare.exact('practice_loc6_zip', 'zipcode', label = 'zip6')
compare.exact('mail_loc_zip', 'zipcode', label = 'zip7')
compare.exact('practice_loc1_phone', 'PhoneNo1', label = 'phone1')
compare.exact('practice_loc2_phone', 'PhoneNo1', label = 'phone2')
compare.exact('practice_loc3_phone', 'PhoneNo1', label = 'phone3')
compare.exact('practice_loc4_phone', 'PhoneNo1', label = 'phone4')
compare.exact('practice_loc5_phone', 'PhoneNo1', label = 'phone5')
compare.exact('practice_loc6_phone', 'PhoneNo1', label = 'phone6')
compare.exact('mail_loc_phone', 'PhoneNo1', label = 'phone7')

# compute comparison
features = compare.compute(candidates, df, pals_providers)

# select pairs w/ at least one matching column
matches = features[features.sum(axis=1) > 1].reset_index() 

# create scoring system
matches['zip_match'] = matches.loc[:, 'zip1':'zip7'].sum(axis=1)
matches['zip_match'] = matches['zip_match'].apply(lambda x: 1 if x > 0 else 0) # indicate pairs with a matching zip

matches['phone_match'] = matches.loc[:, 'phone1':'phone7'].sum(axis=1)
matches['phone_match'] = matches['phone_match'].apply(lambda x: 1 if x > 0 else 0) # indicate pairs with a matching phone

matches['firstmatch'] = matches.loc[:, 'FirstName':'FirstName_alt'].sum(axis = 1)
matches['firstmatch'] = matches['firstmatch'].apply(lambda x: 1 if x > 0 else 0) # indicate whether first or firstname_alt name matches
matches['lastmatch'] = matches.loc[:, 'LastName':'LastName_alt'].sum(axis = 1)
matches['lastmatch'] = matches['lastmatch'].apply(lambda x: 1 if x > 0 else 0)

matches['lastmatch'] *= 2 # weight last name match more heavily

matches['name_score'] = matches[['firstmatch', 'lastmatch', 'MiddleName', 'MidInit', 'FullName_match']].sum(axis=1)

matches['LicenseNumber'] *= 5 # give greatest weight to matching license no

matches['other_score'] = matches[['zip_match', 'phone_match', 'ProfessionType', 'LicenseNumber']].sum(axis=1)

matches['total_score'] = matches['name_score'] + matches['other_score']

# merge in names
matches = matches.merge(df['full_name'], left_on = 'level_0', right_index = True)
matches = matches.merge(pals_providers['FullName'], left_on = 'level_1', right_index = True)

# Keep PALS name w/ highest total score for each NPI name
matches['name_tot_max'] = matches.groupby('full_name')['total_score'].transform('max')

# Drop 3 incorrect matches that seem to be result of out of state licenses matching
matches = matches[~matches['FullName'].str.contains('KAREN M HART|VIRGINIA T SHEPHARD|KELLY SUZANNE RAZLER')]

matches = matches[matches['total_score'] == matches['name_tot_max']]

matches = matches[['FullName', 'full_name']]
matches = matches.drop_duplicates()

# use inner join to drop PALS results that don't match NPI
pals_providers = pals_providers.merge(matches, how = 'inner', on = 'FullName')

# merge in NPI numbers
pals_providers = pals_providers.merge(df[['full_name', 'npi']], how = 'inner', on = 'full_name')

# drop columns used for matches
pals_providers = pals_providers.drop(columns=['full_name', 'MidInit'])


# QUERY 2nd URL to obtain more detailed license info
pals_licenses = pd.DataFrame()
url2 = "https://www.pals.pa.gov/api/SearchLoggedIn/GetPersonOrFacilityDetails"

# loop over 1st url output
for j in pals_providers.index:
    print("License", (j + 1), "of", len(pals_providers.index))
    data2 = {
                'IsFacility': 0,
                'LicenseId': pals_providers['LicenseId'][j],
                'LicenseNumber': pals_providers['LicenseNumber'][j],
                'PersonId': pals_providers['PersonId'][j]
                }

    page2 = requests.post(url2, data2).text
    page2 = json.loads(page2)

    # the disciplinary records seem to be in random order and key info is in PDFs, so for now just flag the people with a record
    if (len(page2['DisciplinaryActionDetails']) > 0):
        page2.update({'More_Info_See_PALS': 'Y'})
    else:
        page2.update({'More_Info_See_PALS': 'N'})

    # remove lists from dict
    rm_list = ['PinItemList', 'PrerequisiteInformation', 'OtherLicenseDetails', 'DisciplinaryActionDetails', 'StatusHistoryList', 'LicenseCSRInformation']

    for key in rm_list:
        del page2[key]

    # append to license datafrmae
    pals_licenses = pals_licenses.append(pd.DataFrame([page2]))


# MERGE OUTPUTS
pals_licenses = pals_licenses[['LicenseId', 'obtainedBy', 'SpecialityType', 'StatusEffectivedate', 'IssueDate', 'ExpiryDate', 'LastRenewalDate', 'More_Info_See_PALS']]

pals_licenses.reset_index(drop=True, inplace=True)
pals_providers.reset_index(drop=True, inplace=True)

final_df = pals_providers.merge(pals_licenses, how='outer', left_index=True, right_index=True, on='LicenseId')

# drop columns that are always empty
final_df = final_df.dropna(axis=1, how='all')

# write tall data to csv
outdate = date.today().strftime('%Y-%m-%d')
outlen = df.shape[0]

final_df.to_csv(os.path.join(path, 'data', f"PALS_tall_{outdate}_{outlen}_.csv"), index=False)

# write no_result to txt
with open(os.path.join(path, 'data', f"PALS_noresult_{outdate}_{outlen}_.txt"), 'w') as nofile:
    nofile.write("No PALS result found for:" + "\n")
    for name in noresult:
        nofile.write(name[0] + " " + name[1] + "\n")


# Use pals_wide.py to create wide version of output