import requests
import pandas as pd
import os
import time

path = os.getcwd()

df = pd.read_csv(os.path.join(path, 'data', 'BupePrescribers_Phila-in-SAMHSA_2019Q4-2020Q2_528recs.csv'), index_col=False)
npi_data = df['dea_num'].values.tolist()
npi_data = ["None" if type(x) == float else str(x) for x in npi_data]
url = 'https://www.samhsa.gov/bupe/lookup-form'
samhsa_data_list = []
counter = 1
for index, row in df.iterrows():
        if counter % 100 == 0:
            time.sleep(300)
        counter +=1
        print(str(int(index)+1), row['npi'])
        dea_number = 'A*' if type(row['dea_num']) == float else str(row['dea_num'])
        data = {'practitioner': row['lastname'],
            'dea_number': dea_number,
            'form_build_id': 'form-MLgZu20sRJX2-p5eYVmVnVpZfuTyu5DgBYQJEVHe1I8',
            'form_id': 'bupe_pharm_lookup',
            'op': 'Submit'}
        page = requests.post(url,data).text
        data_list = []
        data_string = page.split('\\u003Cli class=\\u0022messages__item\\u0022\\u003E')[1:]
        for data in data_string:
            data_list.append(data.split('\\u003C\\/li\\u003E\\n ')[0])
        samsha_data = {}
        if "is not a Buprenorphine Certified Physician" in page:
            samsha_data['Full Name'] = "Not Buprenorphine Certified Physician"
            samsha_data['Job'] = "Not Buprenorphine Certified Physician"
            samsha_data['DEA Registration Number'] = "Not Buprenorphine Certified Physician"
            samsha_data['Licensed State'] = "Not Buprenorphine Certified Physician"
            samsha_data['Date Certified'] = "Not Buprenorphine Certified Physician"
            samsha_data['Waiver Count'] = "Not Buprenorphine Certified Physician"
        else:
            if data_list[0].split(' is a')[0] == (row['firstname'] + ' ' + row['lastname']):
                samsha_data['Full Name'] = data_list[0].split(' is a')[0]
                samsha_data['Job'] = data_list[0].split(' is a ')[1][:-2]
                samsha_data['DEA Registration Number'] = data_list[1].split(': ')[1]
                samsha_data['Licensed State'] = data_list[2].split(': ')[1]
                samsha_data['Date Certified'] = data_list[3].split(': ')[1]
                samsha_data['Waiver Count'] = data_list[4].split('for ')[1].split(' patients')[0]
            else:
                samsha_data['Full Name'] = "Name does not match with SAMHSA result"
                samsha_data['Job'] = "Name does not match with SAMHSA result"
                samsha_data['DEA Registration Number'] = "Name does not match with SAMHSA result"
                samsha_data['Licensed State'] = "Name does not match with SAMHSA result"
                samsha_data['Date Certified'] = "Name does not match with SAMHSA result"
                samsha_data['Waiver Count'] = "Name does not match with SAMHSA result"
        # print(samsha_data)
        samhsa_data_list.append(samsha_data)
final_df = pd.DataFrame(samhsa_data_list)
df = df.reset_index(drop=True)
final_df = pd.concat([df, final_df], axis=1)
final_df.to_csv(os.path.join(path, 'data', 'new_final_hfp_samhsa.csv'), index=False)
