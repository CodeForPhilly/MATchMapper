import requests
import json
import pandas as pd
import math
import os

def adjust_phone_format(phone_number):
    if len(phone_number) > 0 and phone_number[0] == "#":
        phone_number = phone_number[2:]
        phone_number = phone_number.replace(")","-")
    return phone_number

path = os.getcwd()

df = pd.read_csv(path + '\\data\\BupePrescribers_Phila-in-SAMHSA_2019Q4-2020Q2_528recs.csv', index_col=False)
npi_data = df['npi'].values.tolist()
npi_data = [str(int(x)) if not math.isnan(float(x)) else 0 for x in npi_data]
df = df[['who_id']]
npi_final_data = []
counter = 0
for npi_id in npi_data:
    npi_dict = {}
    if npi_id != 0:
        counter +=1
        print(npi_id, counter)
        url = 'https://npiregistry.cms.hhs.gov/api/?version=2.1&number=' + npi_id
        response = requests.get(url)
        json_data = json.loads(response.text)
        assert json_data['result_count'] == 1
        result = json_data['results'][0]
        npi_dict['npi'] = str(result['number'])
        basic_info = result['basic']
        npi_dict.update(basic_info)
        # only work with one other name. could have multiple other names
        if len(result['other_names']) >= 1:
            for key, value in result['other_names'][0].items():
                npi_dict['other_names_' + key] = value
        addresses = result["addresses"]
        # 'LOCATION" address is the primary practicing location while "MAILING" is the mailing address
        for address in addresses:
            if address['address_purpose'] == 'LOCATION':
                prefix = "primary_practice_location_"
            elif address['address_purpose'] == 'MAILING':
                prefix = "mailing_location_"
            else:
                raise ValueError("unknown address purpose")

            for key, value in address.items():
                if key == "telephone_number":
                    npi_dict[prefix + key] = adjust_phone_format(value)
                # some postal code has a 4 digit number behind that I am using '-' to separate from the main 5 digits
                elif key == 'postal_code':
                    if len(value) > 5:
                        npi_dict[prefix + key] = value[:5] + '-' + value[5:]
                    else:
                        npi_dict[prefix + key] = value
                else:
                    npi_dict[prefix + key] = value
                
            
        identifiers = result['identifiers']
        if len(identifiers) > 1:
            npi_dict['identifiers'] = ' | '.join([(x['desc'] + ' (' + x['issuer'] + ') ' + x['state'] + ' ' + x['identifier']) if x['issuer'] is not '' else (x['desc'] + ' ' + x['state'] + ' ' + x['identifier']) for x in identifiers])
        elif len(identifiers) == 1:
            npi_dict['identifiers'] = identifiers[0]['desc'] + ' (' + identifiers[0]['issuer'] + ') ' + identifiers[0]['state'] + ' ' + identifiers[0]['identifier'] if identifiers[0]['issuer'] is not '' else identifiers[0]['desc'] + ' ' + identifiers[0]['state'] + ' ' + identifiers[0]['identifier'] 
        taxonomies = result['taxonomies']
        # this section of code will first try to find taxonomies that are both primary and from PA
        # if it can't find one that fits this requirement, we try to find primary taxonomies
        # if we still can't find primary taxonomies, we settle for PA ones. Worst case, we just take any taxonomy that is there
        if len(taxonomies) >= 1:
            if len([x for x in taxonomies if x['primary'] == True and x['state'] == 'PA']) >= 1:
                taxonomies = [x for x in taxonomies if x['primary'] == True and x['state'] == 'PA']
            elif len([x for x in taxonomies if x['primary'] == True]) >= 1:
                taxonomies = [x for x in taxonomies if x['primary'] == True]
            elif len([x for x in taxonomies if x['state'] == 'PA']) >= 1:
                taxonomies = [x for x in taxonomies if x['state'] == 'PA']                
            npi_dict['primary_taxonomy'] = taxonomies[0]['desc'] 
            npi_dict['primary_taxonomy_code'] = taxonomies[0]['code']
            npi_dict['primary_taxonomy_state'] = taxonomies[0]['state']
            npi_dict['primary_taxonomy_license'] = taxonomies[0]['license']
            if len(result['taxonomies']) > 1:
                for taxonomy in result['taxonomies']:
                    if taxonomy['desc'] != npi_dict['primary_taxonomy']:
                        npi_dict['secondary_taxonomy'] = taxonomy['desc'] 
                        npi_dict['secondary_taxonomy_code'] = taxonomy['code']
                        npi_dict['secondary_taxonomy_state'] = taxonomy['state']
                        npi_dict['secondary_taxonomy_license'] = taxonomy['license']
                        break
        # There could be multiple alternative practice locations but I am only choosing the first one as the secondary practice location
        if result.get('practiceLocations') is not None:
            for key, value in result['practiceLocations'][0].items():
                if key == "telephone_number":
                    npi_dict["secondary_practice_location_" + key] = adjust_phone_format(value)
                elif key == 'postal_code':
                        if len(value) > 5:
                            npi_dict["secondary_practice_location_" + key] = value[:5] + '-' + value[5:]
                        else:
                            npi_dict["secondary_practice_location_" + key] = value
                else:
                    npi_dict["secondary_practice_location_" + key] = value

        
    npi_final_data.append(npi_dict)
final_df = pd.DataFrame(npi_final_data)
df.columns = ['who_id']
df = df.reset_index(drop=True)
final_df = pd.concat([df, final_df], axis=1)
final_df.to_csv(path + "\\data\\new_final_hfp_npi.csv", index=False)

