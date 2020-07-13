import requests
import json

url1 = 'https://www.pals.pa.gov/api/Search/SearchForPersonOrFacilty'
data1 = {
        'Country': "ALL",
        'County': None,
        'FirstName': "",
        'IsFacility': 0,
        'LastName': "",
        'LicenseNumber': "MD015529E",
        'OptPersonFacility': "Person",
        'PageNo': 1,
        'PersonId': None,
        'State': "Pennsylvania"}
page1 = requests.post(url1,data1).json()
print(page1)

url2 = "https://www.pals.pa.gov/api/SearchLoggedIn/GetPersonOrFacilityDetails"
data2 = {
    'IsFacility': str(data1['IsFacility']),
    'LicenseId': page1[0]['LicenseId'],
    'LicenseNumber': data1['LicenseNumber'],
    'PersonId': page1[0]['PersonId']
}
page2 = requests.post(url2, data2).text
print(page2)